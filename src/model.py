import torch
import torch.nn.functional as F
import os
import pytorch_lightning

from transformers import CLIPModel

from src.config import get_cfg

class PatentModel(pytorch_lightning.LightningModule):
    def __init__(self, *, base_model):
        super(PatentModel, self).__init__()
        self.cfg = get_cfg()
        self.model = CLIPModel.from_pretrained(self.cfg.model.base)
    
    def batch_step(self, batch, step, return_loss=False):
        batch = self.transfer_batch_to_device(batch, self.device, 0)
        outputs = self(**batch, return_loss=True)

        distances = F.cosine_similarity(outputs.text_embeds, outputs.image_embeds)

        image_pred = outputs.logits_per_image.argmax(-1)
        text_pred = outputs.logits_per_image.argmax(-1)

        image_accuracy = (image_pred == torch.arange(0, distances.shape[0]).to(self.device)).float().mean()
        text_accuracy = (text_pred == torch.arange(0, distances.shape[0]).to(self.device)).float().mean()
        mean_distance = distances.mean()

        metrics = {
            f"{step}/image_accuracy": image_accuracy.item(),
            f"{step}/text_accuracy": text_accuracy.item(),
            f"{step}/mean_distance": mean_distance.item(),
            f"{step}/loss": outputs.loss.item()
        }
        self.log_dict(metrics)
        
        if return_loss:
            return outputs.loss
        else:
            return metrics

    def training_step(self, batch):
        return self.batch_step(batch, "train", return_loss=True)
    
    def validation_step(self, batch, it):
        return self.batch_step(batch, "validation")
    
    def test_step(self, batch, it):
        return self.batch_step(batch, "test")

    def forward(self, **kwargs):
        return self.model(**kwargs)

    def step(self, step, batch):
        pass

    def configure_optimizers(self):
        optimizer = getattr(torch.optim, self.cfg.optimizer.name)
        return optimizer(self.parameters(), **self.cfg.optimizer.args)


if __name__ == "__main__":
    from src.config import get_cfg
    from src.dataset import PatentDataset, PatentDatasetType
    from torch.utils.data import DataLoader

    ds = PatentDataset(PatentDatasetType.VALIDATION)
    dl = DataLoader(ds, batch_size=4, shuffle=False)

    cfg = get_cfg()
    model = PatentModel(base_model=cfg.model.base)

    model.configure_optimizers()
    for batch in dl:
        model.validation_step(batch, 0)
        loss = model.training_step(batch)
        print(loss)
        loss.backward()
        break
