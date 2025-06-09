import argparse
from fastcoref import LingMessCoref as OriginalLingMessCoref
from transformers import AutoModel
import functools
import re

class PatchedLingMessCoref(OriginalLingMessCoref):
    def __init__(self, *args, **kwargs):
        original_from_config = AutoModel.from_config

        def patched_from_config(config, *args, **kwargs):
            kwargs['attn_implementation'] = 'eager'
            return original_from_config(config, *args, **kwargs)

        try:
            AutoModel.from_config = functools.partial(patched_from_config, attn_implementation='eager')
            super().__init__(*args, **kwargs)
        finally:
            AutoModel.from_config = original_from_config

class Coreference_reslution:
    """
    output: target_entity, target_start, target_end, reference_entity, reference_start, reference_end
    """
    def __init__(self, device):
        self.device = device
        self.model = self._init_coref_model(device)
    
    def _init_coref_model(self, device):
        return PatchedLingMessCoref(
            nlp="en_core_web_lg",
            device=device
        )


    def resolute(self, text):
        """
        Find all the coreference resolution in the given text
        model: coreference resolution model  
        text: input text (only one text)  
        output: target_entity, target_start, reference_entity, reference_start
        """
        output = []
        preds = self.model.predict([text])

        # Split the text into words and punctuation
        words = re.findall(r'\w+|[^\w\s]', text)
        word_positions = []
        current_pos = 0

        for word in words:
            start_pos = text.find(word, current_pos)
            word_positions.append((start_pos, start_pos + len(word)))
            current_pos = start_pos + len(word)

        for pred in preds:
            entities = pred.get_clusters(as_strings=True)
            indices = pred.get_clusters(as_strings=False)
            for entity_group, index_group in zip(entities, indices):
                target_entity = entity_group[0]
                target_start, _ = index_group[0]

                # Convert character position to word position
                target_word_start = next(i for i, (start, end) in enumerate(word_positions) if start <= target_start < end)

                for i, reference_entity in enumerate(entity_group[1:], start=1):
                    reference_start, _ = index_group[i]

                    reference_word_start = next(i for i, (start, end) in enumerate(word_positions) if start <= reference_start < end)

                    output.append([
                        target_entity, target_word_start,
                        reference_entity, reference_word_start
                    ])

        return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="cuda:0")
    parser.add_argument("--input_file", type=str, default="../../test.txt")
    parser.add_argument("--output_file", type=str, default="../../output/Coreference_reso_output.csv")
    args = parser.parse_args()

    # with open(args.input_file, "r") as f:
    #     texts = f.read()
    texts = "Obama is the president of the United States. He was born in Hawaii. He is a good president. Michelle Obama is his wife. She is a lawyer. She is a good wife."
    # collect target_entity,target_start,target_end,reference_entity,reference_start,reference_end
    # [[(0, 48), (185, 187), (246, 251)], [(301, 309), (338, 346)]]
    # e.g. Barack Hussein Obama II[a] (born August 4, 1961), 0, 48, he, 185, 187
    # e.g. Barack Hussein Obama II[a] (born August 4, 1961), 0, 48, he, 246, 251
    coref = Coreference_reslution(args.device)
    output = coref.resolute(texts)
    print(output)


    # print("saving to", args.output_file)
    # df = pd.DataFrame(output, columns=["target_entity", "target_start", "target_end", "reference_entity", "reference_start", "reference_end"])
    # df.to_csv(args.output_file, index=False)

    # for pred in preds:
    #     print(pred.get_clusters(as_strings=True))
    #     print(pred.get_clusters(as_strings=False))

    