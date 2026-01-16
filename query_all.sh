#!/bin/sh

#./query.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-custom query.paths.results=/results/A42B3-custom query.joint=True
#./query.sh query.cls=A62B18 query.model=/models/model.ckpt qdrant.db=/database/A62B18-custom query.paths.results=/results/A62B18-custom
#./query.sh query.cls=F04D17 query.model=/models/model.ckpt qdrant.db=/database/F04D17-custom query.paths.results=/results/F04D17-custom
#./query.sh query.cls=F16H1 query.model=/models/model.ckpt qdrant.db=/database/F16H1-custom query.paths.results=/results/F16H1-custom
#./query.sh query.cls=F16L1 query.model=/models/model.ckpt qdrant.db=/database/F16L1-custom query.paths.results=/results/F16L1-custom
#./query.sh query.cls=G02C5 query.model=/models/model.ckpt qdrant.db=/database/G02C5-custom query.paths.results=/results/G02C5-custom
#./query.sh query.cls=H02K19 query.model=/models/model.ckpt qdrant.db=/database/H02K19-custom query.paths.results=/results/H02K19-custom

#./query.sh query.cls=A42B3 query.model=base qdrant.db=/database/A42B3-base query.paths.results=/results/A42B3-base
#./query.sh query.cls=A62B18 query.model=base qdrant.db=/database/A62B18-base query.paths.results=/results/A62B18-base
#./query.sh query.cls=F04D17 query.model=base qdrant.db=/database/F04D17-base query.paths.results=/results/F04D17-base
#./query.sh query.cls=F16H1 query.model=base qdrant.db=/database/F16H1-base query.paths.results=/results/F16H1-base
#./query.sh query.cls=F16L1 query.model=base qdrant.db=/database/F16L1-base query.paths.results=/results/F16L1-base
#./query.sh query.cls=G02C5 query.model=base qdrant.db=/database/G02C5-base query.paths.results=/results/G02C5-base
#./query.sh query.cls=H02K19 query.model=base qdrant.db=/database/H02K19-base query.paths.results=/results/H02K19-base

#./query.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-H02K19-custom query.paths.results=/results/A42B3-H02K19-custom query.apply_filter=True query.joint=True
#./query.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-F16L1-custom query.paths.results=/results/A42B3-F16L1-custom
#./query.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-custom query.paths.results=/results/A42B3-A62B18-custom

# for ICED paper
./query.sh query.cls=A42B3 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-H02K19-custom query.paths.results=/results/A42B3-A62B18-H02K19-custom query.apply_filter=False query.joint=True
./query.sh query.cls=A62B18 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-H02K19-custom query.paths.results=/results/A42B3-A62B18-H02K19-custom query.apply_filter=False query.joint=True
./query.sh query.cls=H02K19 query.model=/models/model.ckpt qdrant.db=/database/A42B3-A62B18-H02K19-custom query.paths.results=/results/A42B3-A62B18-H02K19-custom query.apply_filter=False query.joint=True

./query.sh query.cls=A42B3 query.model=base qdrant.db=/database/A42B3-A62B18-H02K19-base query.paths.results=/results/A42B3-A62B18-H02K19-base query.apply_filter=False query.joint=True
./query.sh query.cls=A62B18 query.model=base qdrant.db=/database/A42B3-A62B18-H02K19-base query.paths.results=/results/A42B3-A62B18-H02K19-base query.apply_filter=False query.joint=True
./query.sh query.cls=H02K19 query.model=base qdrant.db=/database/A42B3-A62B18-H02K19-base query.paths.results=/results/A42B3-A62B18-H02K19-base query.apply_filter=False query.joint=True
