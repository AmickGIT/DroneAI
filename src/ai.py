import google.generativeai as genai




class AI():
    def __init__(self):
        genai.configure(api_key="AIzaSyD42iTcQnwKnmPquVL-dU_p9664eOtGf_Q")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def process_text(self, text):
        response = self.model.generate_content(f"""Interpret "{text}" in the context of commands for drone control.
                                              Rules:0. The vaild directions are: [up, down, left, right , front, back] and all possible combinations taking 2 at a time.
                                                    1. Anything related to 'fast'/'quick' add the suffix 'and acclerating' after the direction
                                                    2. "constant speed" is the default suffix is words related to "fast" or "slow" are not present
                                                    3. Anything related to 'braking'/'slow' respond with 'STOP' only
                                                    4. If there are multiple interpretations, respond with the last one.
                                                    5. If the text is not related to a command, ex:"but","or" respond with 'no action' only
                                                    6. If "move" or "go" then respond with 'front and constant speed'
                                                    7. If "quickly" then respond with 'front and acclerating' 
                                                    8. If the directions are opposite, ex: "left right quickly" or "up down" or "left right" respond with 'no action'
                                                    9. Never respond with reasoning
                                                    10. For actions like 'do a back flip' respond with no action
                                                    11. "Forwards" or "backwards" is equivalent to "front" and "back"
                                                    12. Words like forward or bottom are equivalent to "front" and "down" respectively.
                                                    13. Words like "dawn", "don", "town" mean "down"
                                                    14. Words like "love" mean "left"
                                                    15. Treat "right" as a direction only
                                                    16. Do not focus on irrelevant or ambiguous words or phrases like [switch, but] etc
                                               Example: If 'go right' then respond with "right and constant speed"
                                                        If 'go quickly to left' respond with "left and acclerating"
                                                        If 'down right' then respond with 'down right and constant speed'
                                                        If 'brake' then respond with "STOP"
                                                        If 'go left and right' respond in context to the latest words, that is "right and constant speed"
                                                        If 'forward' then respond with 'front and constant speed'
                                                        If 'back slowly' respond with 'STOP'
                                                        If 'forward down' respond with 'front down and constant speed'
                                                        If 'back right quickly' respond with "Back right and acclerating"
                                                        If 'up' respond with "up and constant speed"
                                                        If 'bottom' respond with 'down and constant speed'
                                                        If 'Up bottom quickly' respond with 'no action' as they are opposite directions.
                                               """)
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