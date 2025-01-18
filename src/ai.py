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
                                                    6. If "move" then respond with 'front and constant speed'
                                                    7. If the directions are opposite, ex: "left right quickly" or "up down" or "left right" respond with 'no action'
                                                    8. Never respond with reasoning
                                                    9. For actions like 'do a back flip' respond with no action
                                                    10. "Forwards" or "backwards" is equivalent to "front" and "back"
                                                    11. Words like forward or bottom are equivalent to "front" and "down" respectively.
                                                    12. Words like "dawn", "don", "town" mean "down"
                                                    13. Words like "love" mean "left"
                                                    14. Treat "right" as a direction only
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
# ai = AI()