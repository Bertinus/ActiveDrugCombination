# Predicting the effect of drug combinations: an Active Learning Approach

## DrugComb data

We use data from ```http://drugcombdb.denglab.org/download```

Original paper: [link](https://watermark.silverchair.com/gkz1007.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAAqMwggKfBgkqhkiG9w0BBwagggKQMIICjAIBADCCAoUGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMhDWClWOcHgU1fSDbAgEQgIICVrreiMo1vFET4Ud-o-1UUwaPfzHQqcgBX7Wn8cSRydAEroefC2JbPPolK3vZ5SeATnugMTSfTbfKb7btiiuFKOd0CxDl4OUuvVV98FVZkU1LQ0eVDI4b4S3YVwDIjYKrhZEEp9AfWG54ngrcbWAOh08pnYuRaHlQrYsUDW9X4V2s3yoqSfIghDx1br6osNXvK0dWOLf8OJBLWoDCqVBlCDFoRHBT_aQoZCle0h390IZG9wkNp0tD3MMZ3ITaRB9DRLKlR6KfP7s1iBq0slzUcr23JGw1W7OIewFoR8h9y207uOKi7kuHiRC5ecLqFTO_xQPOSL5rrtAKflhZ9TUKul8KD7mw8vRbV2py98t38fqlNICpUdMnBCyVTYWZWNudk47T3fvKwemweQ-3Ca--yH1DOMipl8ib_khqm_rNCsvUrWnBWeHkyNACRbsAL-lOx52TH-QaJupXrzsJA3YfhBeXEEzzwxQnrEb72PHX2yAS0R8YnV8fuFyXWLMA5lZ5kgC_MmiWjJkcohcdO0PxetwFMM50HTuXcy1BVbNfaW1bOfBlvfikDTXVkNbukFXAQsfYFEY_uCNvr-Xr6qh93V7AywGk9reyMAKbqj1qldyz86l1WdTl49g8gBqDjhRPy-QJ2UR1Y5vfbv8Z8K9KqF0Q0Lo4fs1D6oY5FxgcNyzO7d2QSxizWI4N4tIyki7qwveBh9KOQkPoy7utuFvp-xkKcLcQdxmhT2iwbltC9wYO-oUAiUSeemmxp-jyZfu0KDSwTNSkEHNXfcypnjLldq52m2sZ6FA)

Run ````get_drug_comb_data.py```` to download this data

Ressource to understand the different synergy scores: [link](https://www.researchgate.net/publication/282281738_Searching_for_Drug_Synergy_in_Complex_Dose-Response_Landscapes_Using_an_Interaction_Potency_Model/link/560a5b4208ae1396914bba65/download)

## Environment setup

Set up a conda environment for the project using the provided specification file:

```conda create --name myenv --file spec-file.txt```

Note: if you want to generate the fingerprints again using ```generate_fingerprints.py```, you should use another conda environment with ```rdkit``` installed (rdkit is not provided in the specification file)

