# Importer les libraries nécessaires
from openai import OpenAI
responses=['support','oppose','neutral','not relevant','unknown']

# Creer Une Analyzeur qui GPT 3 pourra utiliser pour analyser les tweets
class Analyzer:

    # __init__ prends en parametre le prompt initial qui va données à GPT3 le contexte de la conversation
    def __init__(self, prompt:str):
        self.prompt = prompt
# Analyze prends en parametre le texte à analyser et retourne le résultat de l'analyse. Le resultat a 4
    def analyze(self, tweet:str, user_name:str, user_handle:str):
        tweet_prompt=(
            f"Analyze the following tweet by @{user_handle} ({user_name}):\n"
            f"'{tweet}'\n\n")
        
        
        try:

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages= [{"role": "system", "content": self.prompt},
                    {"role": "user", "content":tweet_prompt}],
                temperature=0,
                max_tokens=10
            )

            #extract the text from the response
            result = int(response.choices[0].message.content)
            print(f"OpenAI response:{responses[result - 1]}")

            if result >= 1 and result <= 5 :
                return responses[result - 1]
            else:
                print(f"unexpected response from OpenAI: {result}")
                return 'unknown'
            
        except Exception as e:
            print(f"Error analyzing tweet: {e}")
            return "unknown"

        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return 'unknown'