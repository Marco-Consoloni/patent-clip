import os
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import WandbLogger
import wandb
from omegaconf import OmegaConf

from src.dataset import PatentDataset, PatentDatasetType
from src.model import PatentModel
from src.config import get_cfg

def main():
    cfg = get_cfg()

    if cfg.train.seed == -1:
        random_data = os.urandom(4)
        seed = int.from_bytes(random_data, byteorder="big")
        cfg.train.seed = seed
    pl.seed_everything(cfg.train.seed)

    loggers = []
    callbacks = []

    if cfg.wandb.log:
        hyperparameters = OmegaConf.to_container(cfg, resolve=True)
        wandb.init(entity=cfg.wandb.entity, project=cfg.wandb.project)
        wandb.config.update(hyperparameters)
        wandb_logger = WandbLogger()
        loggers.append(wandb_logger)

    num_workers = os.cpu_count()
    train_dataset = PatentDataset(PatentDatasetType.TRAIN)
    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=cfg.train.batch_size,
        shuffle=True,
        num_workers=num_workers if cfg.train.num_workers == -1 else cfg.train.num_workers
    )

    val_dataset = PatentDataset(PatentDatasetType.VALIDATION)
    val_dataloader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=cfg.validation.batch_size,
        num_workers=num_workers if cfg.validation.num_workers == -1 else cfg.validation.num_workers
    )

    test_dataset = PatentDataset(PatentDatasetType.TEST)
    test_dataloader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=cfg.test.batch_size,
        num_workers=num_workers if cfg.test.num_workers == -1 else cfg.test.num_workers
    )

    checkpoint_callback = ModelCheckpoint(
        monitor=cfg.early_stop.metric,
        save_top_k=1,
        mode=cfg.early_stop.mode,
        dirpath="models",
        filename="best-checkpoint"
    )
    callbacks.append(checkpoint_callback)

    early_stopping_callback = EarlyStopping(
        monitor=cfg.early_stop.metric,
        patience=cfg.early_stop.patience,
        mode=cfg.early_stop.mode
    )
    callbacks.append(early_stopping_callback)

    model = PatentModel(base_model=cfg.model.base)
    accelerator = "gpu" if (torch.cuda.is_available() and cfg.train.use_gpu) else "cpu"
    trainer = pl.Trainer(
        logger=loggers,
        callbacks=callbacks,
        accelerator=accelerator,
        devices=cfg.train.gpus if accelerator == "gpu" else None,
        max_epochs=cfg.train.max_epochs,
        num_sanity_val_steps=0,
        log_every_n_steps=1,
        val_check_interval=cfg.train.validate_every,
        check_val_every_n_epoch=1,
    )

    trainer.test(model, test_dataloader)
    trainer.fit(model, train_dataloader, val_dataloader)
    trainer.test(model, test_dataloader)

    if cfg.train.save_file != "":
        trainer.save_checkpoint(cfg.train.save_file)

if __name__ == "__main__":
    main()
