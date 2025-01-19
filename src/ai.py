import google.generativeai as genai




class AI():
    def __init__(self):
        genai.configure(api_key="AIzaSyD42iTcQnwKnmPquVL-dU_p9664eOtGf_Q")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def process_text(self, text):
        response = self.model.generate_content(f"""
                                  Respond with '1' if "{statement}" explicitly implies "switch", that is a change between gesture and voice control 
                                  for drones, and '0' otherwise. Ignore directional words and ambiguous terms. 
                                  Do not explain the rules or add commentary—just respond with '1' or '0' directly. Respond
                                  with '0' is the text does not contain the word "switch" or its tenses like "switching", "switched". 
                                  Search only for the tenses of "switch".
                                  
                                  Example:
                                  If 'right' then respond with '0' because right is a directional word and doesn't imply switching"
                                  If 'that works' then respond with '0' because 'that' works doesn't explicitly mean switching
                                  If 'switch' then respond with '1' as switch explicitly means switching
                                  If 'don't switch' then respond with '0' as don't switch means not switching
                                  If 'go to gesture control' respond with '0' as the word 'switch' is not present
                                  If 'switched' then respond with '1' because it containds words related to 'switch' that is 'switched'""")
        interpreted_text = response.text.strip()
        if interpreted_text == 'no action':
            return None
        elif len(interpreted_text) < 40:
            return interpreted_text
        else:
            return None
    
    def check_for_switch(self, statement):
        response = self.model.generate_content(f"""
                                  Respond with '1' if "{statement}" explicitly implies "switch", that is a change between gesture and voice control 
                                  for drones, and '0' otherwise. Ignore directional words and ambiguous terms. 
                                  Do not explain the rules or add commentary—just respond with '1' or '0' directly. Respond
                                  with '0' is the text does not contain the word "switch" or its tenses like "switching", "switched". 
                                  Search only for the tenses of "switch".
                                  
                                  Example:
                                  If 'right' then respond with '0' because right is a directional word and doesn't imply switching"
                                  If 'that works' then respond with '0' because 'that' works doesn't explicitly mean switching
                                  If 'switch' then respond with '1' as switch explicitly means switching
                                  If 'don't switch' then respond with '0' as don't switch means not switching
                                  If 'go to gesture control' respond with '0' as the word 'switch' is not present
                                  If 'switched' then respond with '1' because it containds words related to 'switch' that is 'switched'""")
        switching_command = response.text.strip()
        if len(switching_command) > 1:
            return None
        else:
            return switching_command
# ai = AI()