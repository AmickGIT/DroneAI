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
        return response.text
    
    def check_for_switch(self, statement):
        response = self.model.generate_content(f"""Context: Switching between gesture control and voice control, for drones.
                                  Rules: 
                                  1.If "{statement}" means switching, respond with '1'.
                                  2.If not then respond with '0'
                                  3.If {statement} is contradictory to "switching" and non-standard rule, then respond with '0'
                                  4.Dp not Give reasoning and respond with 0 or 1
                                  5.Do not focus on irrelevant or ambiguous words
                                  6.Words like "which", "with", "twitch", "batch", "rich", "such", "sewage", "woods" etc mean "switch".
                                  7. I no input rules apply, respond with '0'
                                  
                            
                                  Examples: 
                                  If 'switch' respond with '1' 
                                  If 'switch quickly' respond with '1'
                                  If 'don't switch' respond with '0'
                                  If 'do not switch hello' respond with '0' by ignoring 'hello' as it is ambiguous
                                  If 'that works' respond with '0' as there is no connection between switching and that works""")
        return response.text
# ai = AI()