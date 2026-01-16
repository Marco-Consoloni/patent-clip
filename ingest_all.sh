#!/bin/sh

rm -rf ./docker/database/*

#./ingest.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-custom
#./ingest.sh query.cls=A62B18 query.model=/models/model.ckpt qdrant.db=/database/A62B18-custom
#./ingest.sh query.cls=F04D17 query.model=/models/model.ckpt qdrant.db=/database/F04D17-custom
#./ingest.sh query.cls=F16H1 query.model=/models/model.ckpt qdrant.db=/database/F16H1-custom
#./ingest.sh query.cls=F16L1 query.model=/models/model.ckpt qdrant.db=/database/F16L1-custom
#./ingest.sh query.cls=G02C5 query.model=/models/model.ckpt qdrant.db=/database/G02C5-custom
#./ingest.sh query.cls=H02K19 query.model=/models/model.ckpt qdrant.db=/database/H02K19-custom


#./ingest.sh query.cls=A42B3 query.model=base qdrant.db=/database/A42B3-base
#./ingest.sh query.cls=A62B18 query.model=base qdrant.db=/database/A62B18-base
#./ingest.sh query.cls=F04D17 query.model=base qdrant.db=/database/F04D17-base
#./ingest.sh query.cls=F16H1 query.model=base qdrant.db=/database/F16H1-base
#./ingest.sh query.cls=F16L1 query.model=base qdrant.db=/database/F16L1-base
#./ingest.sh query.cls=G02C5 query.model=base qdrant.db=/database/G02C5-base
#./ingest.sh query.cls=H02K19 query.model=base qdrant.db=/database/H02K19-base

# easy
#./ingest.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-H02K19-custom
#./ingest.sh query.cls=H02K19 query.model=/models/model.ckpt qdrant.db=/database/A42B3-H02K19-custom

# mild easy
#./ingest.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-F16L1-custom
#./ingest.sh query.cls=F16L1 query.model=/models/model.ckpt qdrant.db=/database/A42B3-F16L1-custom

# medium
#./ingest.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-custom
#./ingest.sh query.cls=A62B18 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-custom

# all custom model
#./ingest.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/all-custom
#./ingest.sh query.cls=A62B18 query.model=/models/model.ckpt qdrant.db=/database/all-custom
#./ingest.sh query.cls=F04D17 query.model=/models/model.ckpt qdrant.db=/database/all-custom
#./ingest.sh query.cls=F16H1 query.model=/models/model.ckpt qdrant.db=/database/all-custom
#./ingest.sh query.cls=F16L1 query.model=/models/model.ckpt qdrant.db=/database/all-custom
#./ingest.sh query.cls=G02C5 query.model=/models/model.ckpt qdrant.db=/database/all-custom
#./ingest.sh query.cls=H02K19 query.model=/models/model.ckpt qdrant.db=/database/all-custom

# for ICED paper
./ingest.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-H02K19-custom
./ingest.sh query.cls=A62B18 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-H02K19-custom
./ingest.sh query.cls=H02K19 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-H02K19-custom

./ingest.sh query.cls=A42B3 query.model=base qdrant.db=/database/A42B3-A62B18-H02K19-base
./ingest.sh query.cls=A62B18 query.model=base qdrant.db=/database/A42B3-A62B18-H02K19-base
./ingest.sh query.cls=H02K19 query.model=base qdrant.db=/database/A42B3-A62B18-H02K19-base
