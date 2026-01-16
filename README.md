# Patent CLIP 

This repository contains the code used for developing a proof-of-concept for a multimodal patent retrieval system. It is part of the following published work: 

*"Consoloni, M., Giordano, V., Galatolo, F. A., Cimino, M. G. C. A., & Fantoni, G. (2025). Uncovering the limits of visual-language models in engineering knowledge representation. Proceedings of the Design Society, 5, 3261-3270.* https://doi.org/10.1017/pds.2025.10340" 

It was also submitted to the CodeFest2024 of the European Patent Office on Generative AI: https://www.epo.org/en/news-events/in-focus/codefest/codefest-2024-generative-ai 

## Project Overview
The goal of the project is to develop a multimodal information retrieval system that can use both patent images and text to search patent databases. Existing approaches for information retrieval applied on patents have overlooked the potential of analyzing patent drawings in conjunction with textual data to enhance the accuracy of prior art searches. Moreover, querying patent databases directly with images is not currently supported by these commercial search platforms since drawings cannot be indexed or searched in the same way as text. 

As shown in Fig. 1, the system queries a patent database containing (text, image) pairs, allowing the model to identify the patent images and text most similar to the input query. 

![multimodal_patent_retrieval](assets/multimodal_patent_retrieval.png)

**Fig. 1** - *Multimodal Patent Search Engine.*

The system is based on fine-tuning the foundational vision–language model developed by OpenAI, namely Contrastive Language–Image Pre-training (CLIP), on 1.5M text–image pairs, and includes the scripts for testing and analyzing its performance (see associated publication).









