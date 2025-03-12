from openai import OpenAI

from wsd.models.baseline import JMDict


class OpenAiWordSenseClassifier(OpenAI):
    """
    A ChatGPT base model that classifies words into senses from a dictionary.
    """

    system_prompt = (
        "You are a linguist working on word sense disambiguation. "
        "given a word and context, select the most likely sense."
        "return the probability for the most likey sense."
    )

    def __init__(
        self,
        api_key,
        *args,
        openai_model='gpt-4o-mini',
        temperature=0,
        **kwargs
    ):
        super().__init__(api_key=api_key, *args, **kwargs)
        self.openai_model = openai_model
        self.temperature = temperature

    def predict_proba(self,word : str, context : str, senses : list):
        """
        Returns the probability that the word pairs have the same meaning.

        Parameters
        ----------
        word_pairs: List[WordPairWithContext]
            A list of word pairs to assess.

        Returns
        -------
        preds: Iterable[float]
            Probabilities that each pair has the same meaning.
        """

        #--------------------
        # OLD CODE BELOW (pairwise comparison)
        #--------------------

        # preds = []
        # for cp in candidate_pairs:
        #     user_prompt = (
        #         f"word_1: {cp[0].text}; context_1: {cp[0].context}\n"
        #         f"word_2: {cp[1].text}; context_2: {cp[1].context}"
        #     )
        #     response = self.beta.chat.completions.parse(
        #         model=self.openai_model,
        #         messages=[
        #             {'role': 'system', 'content': self.system_prompt},
        #             {'role': 'user', 'content': user_prompt}
        #         ],
        #         temperature=self.temperature,
        #         max_tokens=2000,
        #         top_p=1,
        #         frequency_penalty=0,
        #         presence_penalty=0,
        #         response_format=ProbaOutput
        #     )
        #     json_str = response.choices[0].message.content
        #     data = json.loads(json_str)
        #     preds.append(data['value'])
        return preds
