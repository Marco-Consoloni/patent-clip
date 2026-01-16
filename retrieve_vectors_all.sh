#!/bin/sh

#./retrieve_vectors.sh retrieve.cls=A42B3 retrieve.collection=text qdrant.db=/database/A42B3-custom retrieve.paths.vectors=/vectors/A42B3-custom
#./retrieve_vectors.sh retrieve.cls=H02K19 retrieve.collection=text qdrant.db=/database/H02K19-custom retrieve.paths.vectors=/vectors/H02K19-custom
./retrieve_vectors.sh retrieve.cls=all retrieve.collection=text qdrant.db=/database/all-custom retrieve.paths.vectors=/vectors/all-custom
./retrieve_vectors.sh retrieve.cls=all retrieve.collection=images qdrant.db=/database/all-custom retrieve.paths.vectors=/vectors/all-custom
./retrieve_vectors.sh retrieve.cls=all retrieve.collection=joint qdrant.db=/database/all-custom retrieve.paths.vectors=/vectors/all-custom

