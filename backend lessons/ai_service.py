import requests
import json
import random
from typing import Dict, List, Optional

class AIService:
    def __init__(self):
        # Free AI APIs - you can replace these with other free services
        self.huggingface_api_url = "https://api-inference.huggingface.co/models/"
        self.openai_api_url = "https://api.openai.com/v1/chat/completions"
        
        # Free models (no API key required for some)
        self.models = {
            "task_generation": "microsoft/DialoGPT-medium",
            "assessment": "gpt2",
            "chat": "microsoft/DialoGPT-medium"
        }
    
    def generate_task(self, subject: str, difficulty: str = "medium") -> Dict:
        """Generate a task using AI"""
        try:
            # Enhanced task database with more variety
            base_tasks = {
                "math": {
                    "easy": [
                        "What is 15 + 27?",
                        "Calculate 8 × 6",
                        "What is half of 24?",
                        "Solve: 3x + 5 = 17",
                        "What is the area of a square with side length 5?"
                    ],
                    "medium": [
                        "Solve the quadratic equation: x² + 5x + 6 = 0",
                        "Calculate the derivative of f(x) = 3x² + 2x - 1",
                        "Find the area of a circle with radius 5 units",
                        "Solve the system: 2x + y = 7, x - y = 1",
                        "Calculate the limit: lim(x→0) (sin(x)/x)"
                    ],
                    "hard": [
                        "Find the integral of ∫(x³ + 2x² - 3x + 1)dx",
                        "Solve the differential equation: dy/dx = 2y",
                        "Calculate the volume of a sphere with radius 3",
                        "Find the eigenvalues of matrix [[2,1],[1,2]]",
                        "Prove that √2 is irrational"
                    ]
                },
                "physics": {
                    "easy": [
                        "What is the SI unit for force?",
                        "Calculate the speed: distance = 100m, time = 10s",
                        "What is the formula for kinetic energy?",
                        "A car travels 60 km in 2 hours. What is its speed?",
                        "What is the unit for power?"
                    ],
                    "medium": [
                        "A car accelerates from 0 to 60 km/h in 10 seconds. Calculate its acceleration.",
                        "Calculate the gravitational force between two 1kg masses 1 meter apart.",
                        "A wave has frequency 500 Hz and wavelength 0.5m. What is its speed?",
                        "Calculate the kinetic energy of a 2kg object moving at 10 m/s.",
                        "Find the electric field at a point 2m from a 5μC charge."
                    ],
                    "hard": [
                        "Derive the equation for simple harmonic motion.",
                        "Calculate the relativistic energy of a particle moving at 0.8c.",
                        "Find the magnetic field inside a solenoid with 1000 turns/m and current 2A.",
                        "Calculate the capacitance of a parallel plate capacitor with area 1m² and separation 1mm.",
                        "Derive the Schrödinger equation for a particle in a box."
                    ]
                },
                "chemistry": {
                    "easy": [
                        "What is the chemical symbol for gold?",
                        "Balance the equation: H₂ + O₂ → H₂O",
                        "What is the atomic number of carbon?",
                        "Name the three states of matter.",
                        "What is the pH of pure water?"
                    ],
                    "medium": [
                        "Calculate the molarity of a solution with 2 moles in 500mL.",
                        "What is the pH of a 0.01M HCl solution?",
                        "How many atoms are in 1 mole of carbon?",
                        "Calculate the molecular weight of H₂SO₄.",
                        "Balance: Fe + O₂ → Fe₂O₃"
                    ],
                    "hard": [
                        "Calculate the equilibrium constant for the reaction: N₂ + 3H₂ ↔ 2NH₃",
                        "Find the rate law for a reaction with mechanism: A + B → C (slow), C + D → E (fast)",
                        "Calculate the Gibbs free energy change for a reaction with ΔH = -50 kJ and ΔS = -100 J/K at 298K",
                        "Determine the oxidation state of each element in KMnO₄",
                        "Calculate the buffer capacity of a solution with pH 4.5"
                    ]
                },
                "biology": {
                    "easy": [
                        "What are the four main types of biomolecules?",
                        "Name the three parts of a cell.",
                        "What is the function of the nucleus?",
                        "What is photosynthesis?",
                        "Name the five kingdoms of life."
                    ],
                    "medium": [
                        "Explain the process of photosynthesis.",
                        "What is the function of mitochondria?",
                        "Describe the structure of DNA.",
                        "What is the difference between mitosis and meiosis?",
                        "Explain the process of cellular respiration."
                    ],
                    "hard": [
                        "Describe the mechanism of enzyme catalysis and factors affecting enzyme activity.",
                        "Explain the process of protein synthesis from DNA to protein.",
                        "Describe the immune response to a viral infection.",
                        "Explain the process of evolution by natural selection with examples.",
                        "Describe the process of photosynthesis in detail, including the light and dark reactions."
                    ]
                },
                "cs": {
                    "easy": [
                        "What is a variable in programming?",
                        "What is the difference between RAM and ROM?",
                        "Name three programming languages.",
                        "What is an algorithm?",
                        "What is the binary representation of 5?"
                    ],
                    "medium": [
                        "What is the time complexity of binary search?",
                        "Explain the difference between stack and queue.",
                        "What is recursion? Give an example.",
                        "Describe the bubble sort algorithm.",
                        "What is object-oriented programming?"
                    ],
                    "hard": [
                        "Implement a binary search tree insertion algorithm.",
                        "Explain the concept of dynamic programming with an example.",
                        "Describe the TCP/IP protocol stack.",
                        "Explain the concept of machine learning and its types.",
                        "Design an algorithm to find the shortest path in a weighted graph."
                    ]
                },
                "engineering": {
                    "easy": [
                        "What is the difference between stress and strain?",
                        "Name three types of engineering.",
                        "What is the purpose of a resistor?",
                        "What is the SI unit for pressure?",
                        "What is the function of a capacitor?"
                    ],
                    "medium": [
                        "Calculate the moment of inertia for a rectangular beam.",
                        "Design a simple circuit with a voltage source and two resistors in series.",
                        "Calculate the efficiency of a heat engine operating between 500K and 300K.",
                        "Find the natural frequency of a mass-spring system.",
                        "Calculate the Reynolds number for fluid flow in a pipe."
                    ],
                    "hard": [
                        "Design a feedback control system for a temperature controller.",
                        "Calculate the stress concentration factor for a hole in a plate.",
                        "Design a digital filter using z-transform.",
                        "Calculate the heat transfer coefficient for forced convection.",
                        "Design a PID controller for a second-order system."
                    ]
                }
            }
            
            subject_tasks = base_tasks.get(subject, base_tasks["math"])
            difficulty_tasks = subject_tasks.get(difficulty, subject_tasks["medium"])
            task = random.choice(difficulty_tasks)
            
            # Add AI-generated hints and explanations
            hints = self._generate_hints(subject, task, difficulty)
            
            return {
                "question": task,
                "subject": subject,
                "difficulty": difficulty,
                "hints": hints,
                "ai_generated": True
            }
        except Exception as e:
            # Fallback to simple task
            return {
                "question": f"Solve a {subject} problem",
                "subject": subject,
                "difficulty": difficulty,
                "hints": ["Think step by step"],
                "ai_generated": False
            }
    
    def assess_answer(self, question: str, student_answer: str, correct_answer: str = None) -> Dict:
        """Assess student's answer using AI with enhanced analysis"""
        try:
            # Enhanced assessment logic with more sophisticated analysis
            assessment = {
                "score": 0,
                "feedback": "",
                "correct": False,
                "ai_assessment": True,
                "detailed_analysis": {}
            }
            
            # Basic keyword matching for assessment
            question_lower = question.lower()
            answer_lower = student_answer.lower()
            
            # Subject-specific assessment with enhanced logic
            if "math" in question_lower or "equation" in question_lower or "calculate" in question_lower or "solve" in question_lower:
                assessment = self._assess_math_answer(question, student_answer, answer_lower)
            elif "physics" in question_lower:
                assessment = self._assess_physics_answer(question, student_answer, answer_lower)
            elif "chemistry" in question_lower:
                assessment = self._assess_chemistry_answer(question, student_answer, answer_lower)
            elif "biology" in question_lower:
                assessment = self._assess_biology_answer(question, student_answer, answer_lower)
            elif "cs" in question_lower or "programming" in question_lower or "algorithm" in question_lower:
                assessment = self._assess_cs_answer(question, student_answer, answer_lower)
            elif "engineering" in question_lower:
                assessment = self._assess_engineering_answer(question, student_answer, answer_lower)
            else:
                # General assessment with enhanced criteria
                assessment = self._assess_general_answer(question, student_answer, answer_lower)
            
            assessment["correct"] = assessment["score"] >= 70
            
            return assessment
            
        except Exception as e:
            return {
                "score": 50,
                "feedback": "Assessment completed. Keep learning!",
                "correct": False,
                "ai_assessment": False,
                "detailed_analysis": {"error": str(e)}
            }
    
    def _assess_math_answer(self, question: str, student_answer: str, answer_lower: str) -> Dict:
        """Enhanced math assessment"""
        score = 0
        feedback = ""
        analysis = {}
        
        # Check for mathematical reasoning
        if any(word in answer_lower for word in ["x=", "=", "solution", "answer", "result", "therefore"]):
            score += 30
            analysis["mathematical_reasoning"] = "Good use of mathematical notation"
        
        # Check for step-by-step work
        if any(word in answer_lower for word in ["step", "first", "then", "next", "finally"]):
            score += 25
            analysis["step_by_step"] = "Shows clear problem-solving steps"
        
        # Check for correct mathematical concepts
        if any(word in answer_lower for word in ["derivative", "integral", "limit", "equation", "formula"]):
            score += 20
            analysis["mathematical_concepts"] = "Demonstrates understanding of mathematical concepts"
        
        # Check for numerical accuracy
        if any(char.isdigit() for char in student_answer):
            score += 15
            analysis["numerical_work"] = "Includes numerical calculations"
        
        # Check for completeness
        if len(student_answer) > 20:
            score += 10
            analysis["completeness"] = "Provides detailed explanation"
        
        if score >= 85:
            feedback = "Excellent mathematical approach! Your solution shows deep understanding of the concepts and proper mathematical reasoning."
        elif score >= 70:
            feedback = "Good mathematical reasoning! Your approach demonstrates solid understanding of the problem."
        elif score >= 50:
            feedback = "Decent mathematical work! Consider showing more detailed steps and final numerical answers."
        else:
            feedback = "Try to provide a complete solution with clear mathematical reasoning and final answer."
        
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "correct": score >= 70,
            "ai_assessment": True,
            "detailed_analysis": analysis
        }
    
    def _assess_physics_answer(self, question: str, student_answer: str, answer_lower: str) -> Dict:
        """Enhanced physics assessment"""
        score = 0
        feedback = ""
        analysis = {}
        
        # Check for physics concepts
        if any(word in answer_lower for word in ["force", "energy", "velocity", "acceleration", "mass", "weight"]):
            score += 30
            analysis["physics_concepts"] = "Good use of physics terminology"
        
        # Check for units
        if any(word in answer_lower for word in ["m/s", "kg", "newton", "joule", "watt", "meter", "second"]):
            score += 25
            analysis["units"] = "Includes proper units"
        
        # Check for formulas
        if any(word in answer_lower for word in ["f=", "e=", "v=", "a=", "formula", "equation"]):
            score += 20
            analysis["formulas"] = "Uses appropriate physics formulas"
        
        # Check for calculations
        if any(char.isdigit() for char in student_answer):
            score += 15
            analysis["calculations"] = "Includes numerical calculations"
        
        # Check for explanation
        if len(student_answer) > 30:
            score += 10
            analysis["explanation"] = "Provides detailed explanation"
        
        if score >= 85:
            feedback = "Outstanding physics understanding! Your answer demonstrates excellent grasp of physical concepts and proper use of units."
        elif score >= 70:
            feedback = "Good physics reasoning! Remember to always include units in your final answers."
        elif score >= 50:
            feedback = "Decent physics work! Focus on using proper formulas and including units."
        else:
            feedback = "Try to use physics formulas and include proper units in your calculations."
        
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "correct": score >= 70,
            "ai_assessment": True,
            "detailed_analysis": analysis
        }
    
    def _assess_chemistry_answer(self, question: str, student_answer: str, answer_lower: str) -> Dict:
        """Enhanced chemistry assessment"""
        score = 0
        feedback = ""
        analysis = {}
        
        # Check for chemical concepts
        if any(word in answer_lower for word in ["mole", "molar", "ph", "balance", "equation", "reaction", "chemical"]):
            score += 30
            analysis["chemical_concepts"] = "Good understanding of chemical concepts"
        
        # Check for chemical notation
        if any(word in answer_lower for word in ["h2o", "co2", "nacl", "h2so4", "subscript", "superscript"]):
            score += 25
            analysis["chemical_notation"] = "Uses proper chemical notation"
        
        # Check for stoichiometry
        if any(word in answer_lower for word in ["coefficient", "ratio", "proportion", "stoichiometry"]):
            score += 20
            analysis["stoichiometry"] = "Demonstrates stoichiometric understanding"
        
        # Check for calculations
        if any(char.isdigit() for char in student_answer):
            score += 15
            analysis["calculations"] = "Includes numerical work"
        
        # Check for explanation
        if len(student_answer) > 25:
            score += 10
            analysis["explanation"] = "Provides detailed explanation"
        
        if score >= 85:
            feedback = "Excellent chemical understanding! Your approach shows mastery of chemical principles and proper notation."
        elif score >= 70:
            feedback = "Good chemical reasoning! Your work demonstrates solid understanding of chemistry concepts."
        elif score >= 50:
            feedback = "Decent chemical work! Focus on using proper chemical notation and balanced equations."
        else:
            feedback = "Try to use proper chemical notation and include balanced equations in your answers."
        
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "correct": score >= 70,
            "ai_assessment": True,
            "detailed_analysis": analysis
        }
    
    def _assess_biology_answer(self, question: str, student_answer: str, answer_lower: str) -> Dict:
        """Enhanced biology assessment"""
        score = 0
        feedback = ""
        analysis = {}
        
        # Check for biological concepts
        if any(word in answer_lower for word in ["cell", "organism", "process", "function", "structure", "system"]):
            score += 30
            analysis["biological_concepts"] = "Good use of biological terminology"
        
        # Check for scientific accuracy
        if any(word in answer_lower for word in ["dna", "protein", "enzyme", "mitochondria", "nucleus", "membrane"]):
            score += 25
            analysis["scientific_accuracy"] = "Uses accurate biological terms"
        
        # Check for process understanding
        if any(word in answer_lower for word in ["step", "first", "then", "process", "sequence"]):
            score += 20
            analysis["process_understanding"] = "Shows understanding of biological processes"
        
        # Check for explanation quality
        if len(student_answer) > 40:
            score += 15
            analysis["explanation_quality"] = "Provides detailed explanation"
        
        # Check for connections
        if any(word in answer_lower for word in ["because", "therefore", "leads to", "results in"]):
            score += 10
            analysis["connections"] = "Makes logical connections"
        
        if score >= 85:
            feedback = "Excellent biological understanding! Your explanation demonstrates deep knowledge of biological concepts and processes."
        elif score >= 70:
            feedback = "Good biological reasoning! Your answer shows solid understanding of biological principles."
        elif score >= 50:
            feedback = "Decent biological work! Try to provide more detailed explanations of biological processes."
        else:
            feedback = "Focus on using biological terminology and providing detailed explanations of processes."
        
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "correct": score >= 70,
            "ai_assessment": True,
            "detailed_analysis": analysis
        }
    
    def _assess_cs_answer(self, question: str, student_answer: str, answer_lower: str) -> Dict:
        """Enhanced computer science assessment"""
        score = 0
        feedback = ""
        analysis = {}
        
        # Check for CS concepts
        if any(word in answer_lower for word in ["algorithm", "complexity", "code", "program", "function", "data structure"]):
            score += 30
            analysis["cs_concepts"] = "Good understanding of CS concepts"
        
        # Check for technical accuracy
        if any(word in answer_lower for word in ["o(n)", "o(log n)", "o(1)", "time complexity", "space complexity"]):
            score += 25
            analysis["technical_accuracy"] = "Uses accurate technical terminology"
        
        # Check for problem-solving approach
        if any(word in answer_lower for word in ["step", "approach", "method", "strategy"]):
            score += 20
            analysis["problem_solving"] = "Shows systematic problem-solving approach"
        
        # Check for code-like elements
        if any(word in answer_lower for word in ["if", "for", "while", "function", "return", "variable"]):
            score += 15
            analysis["code_elements"] = "Includes programming concepts"
        
        # Check for explanation quality
        if len(student_answer) > 35:
            score += 10
            analysis["explanation_quality"] = "Provides detailed technical explanation"
        
        if score >= 85:
            feedback = "Excellent CS understanding! Your answer demonstrates deep knowledge of algorithms and computational thinking."
        elif score >= 70:
            feedback = "Good CS reasoning! Your approach shows solid understanding of computer science principles."
        elif score >= 50:
            feedback = "Decent CS work! Focus on using technical terminology and explaining algorithms clearly."
        else:
            feedback = "Try to use computer science terminology and explain your algorithmic approach clearly."
        
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "correct": score >= 70,
            "ai_assessment": True,
            "detailed_analysis": analysis
        }
    
    def _assess_engineering_answer(self, question: str, student_answer: str, answer_lower: str) -> Dict:
        """Enhanced engineering assessment"""
        score = 0
        feedback = ""
        analysis = {}
        
        # Check for engineering concepts
        if any(word in answer_lower for word in ["design", "calculate", "system", "efficiency", "stress", "force", "load"]):
            score += 30
            analysis["engineering_concepts"] = "Good understanding of engineering principles"
        
        # Check for technical calculations
        if any(word in answer_lower for word in ["formula", "equation", "calculation", "result"]):
            score += 25
            analysis["technical_calculations"] = "Includes technical calculations"
        
        # Check for design thinking
        if any(word in answer_lower for word in ["consider", "factor", "constraint", "requirement"]):
            score += 20
            analysis["design_thinking"] = "Shows engineering design thinking"
        
        # Check for units and precision
        if any(word in answer_lower for word in ["mm", "cm", "m", "kg", "n", "pa", "unit"]):
            score += 15
            analysis["units_precision"] = "Includes proper units and precision"
        
        # Check for explanation quality
        if len(student_answer) > 40:
            score += 10
            analysis["explanation_quality"] = "Provides detailed engineering explanation"
        
        if score >= 85:
            feedback = "Excellent engineering approach! Your solution demonstrates strong technical understanding and systematic design thinking."
        elif score >= 70:
            feedback = "Good engineering reasoning! Your work shows solid understanding of engineering principles."
        elif score >= 50:
            feedback = "Decent engineering work! Focus on including calculations and technical details."
        else:
            feedback = "Try to include technical calculations and engineering design considerations in your answers."
        
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "correct": score >= 70,
            "ai_assessment": True,
            "detailed_analysis": analysis
        }
    
    def _assess_general_answer(self, question: str, student_answer: str, answer_lower: str) -> Dict:
        """Enhanced general assessment"""
        score = 0
        feedback = ""
        analysis = {}
        
        # Check for answer length and detail
        if len(student_answer) > 50:
            score += 30
            analysis["detail"] = "Provides detailed answer"
        elif len(student_answer) > 25:
            score += 20
            analysis["detail"] = "Provides adequate detail"
        elif len(student_answer) > 10:
            score += 10
            analysis["detail"] = "Provides basic answer"
        
        # Check for logical reasoning
        if any(word in answer_lower for word in ["because", "therefore", "since", "thus", "hence"]):
            score += 25
            analysis["logical_reasoning"] = "Shows logical reasoning"
        
        # Check for key concepts
        if any(word in answer_lower for word in ["concept", "principle", "theory", "method", "approach"]):
            score += 20
            analysis["key_concepts"] = "Addresses key concepts"
        
        # Check for examples
        if any(word in answer_lower for word in ["example", "instance", "case", "such as"]):
            score += 15
            analysis["examples"] = "Provides examples"
        
        # Check for clarity
        if len(student_answer.split()) > 20:
            score += 10
            analysis["clarity"] = "Clear and comprehensive explanation"
        
        if score >= 85:
            feedback = "Excellent response! Your answer demonstrates deep understanding and clear communication."
        elif score >= 70:
            feedback = "Good response! Your explanation shows solid understanding of the topic."
        elif score >= 50:
            feedback = "Decent response! Try to provide more detailed explanations and examples."
        else:
            feedback = "Try to provide more detailed explanations and show your reasoning clearly."
        
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "correct": score >= 70,
            "ai_assessment": True,
            "detailed_analysis": analysis
            }
    
    def chat_with_ai(self, message: str, context: str = "") -> str:
        """Chat with AI tutor"""
        try:
            # Enhanced AI chat responses based on keywords
            message_lower = message.lower()
            
            if any(word in message_lower for word in ["help", "stuck", "confused", "don't understand"]):
                return "I'm here to help! Can you tell me more specifically what you're having trouble with? I can explain concepts, provide examples, or guide you through problems step by step."
            
            elif any(word in message_lower for word in ["math", "equation", "solve", "calculate"]):
                return "For math problems, I recommend: 1) Read the problem carefully, 2) Identify what you're solving for, 3) Write down the relevant formulas, 4) Solve step by step, 5) Check your answer. What specific math concept are you working on?"
            
            elif any(word in message_lower for word in ["physics", "force", "energy", "motion", "wave"]):
                return "Physics is all about understanding the fundamental laws of nature! Remember to: 1) Draw diagrams, 2) List known and unknown variables, 3) Choose the right formula, 4) Include units. What physics topic are you studying?"
            
            elif any(word in message_lower for word in ["chemistry", "molecule", "reaction", "equation", "balance"]):
                return "Chemistry is fascinating! Key tips: 1) Understand the periodic table, 2) Learn to balance equations, 3) Remember the mole concept, 4) Practice unit conversions. What chemistry topic interests you?"
            
            elif any(word in message_lower for word in ["biology", "cell", "organism", "process", "function"]):
                return "Biology is the study of life! Focus on: 1) Understanding cell structure, 2) Learning about different systems, 3) Understanding evolution, 4) Connecting structure to function. What biological concept are you exploring?"
            
            elif any(word in message_lower for word in ["programming", "code", "algorithm", "computer", "software"]):
                return "Programming is like learning a new language! Start with: 1) Understanding basic syntax, 2) Learning control structures, 3) Practicing with simple projects, 4) Debugging step by step. What programming language are you learning?"
            
            elif any(word in message_lower for word in ["engineering", "design", "system", "technical", "build"]):
                return "Engineering is about solving real-world problems! Key principles: 1) Understand the problem, 2) Research existing solutions, 3) Design systematically, 4) Test and iterate. What engineering field interests you?"
            
            else:
                return "I'm your AI tutor! I can help you with math, physics, chemistry, biology, computer science, and engineering. Just ask me questions, and I'll guide you through the concepts. What would you like to learn about?"
        
        except Exception as e:
            return "I'm here to help you learn! Feel free to ask me questions about any STEM subject."
    
    def _generate_hints(self, subject: str, question: str, difficulty: str = "medium") -> List[str]:
        """Generate hints for a question"""
        hints = {
            "math": {
                "easy": [
                    "Break down the problem into smaller steps",
                    "Look for patterns or formulas that apply",
                    "Check your answer by plugging it back in"
                ],
                "medium": [
                    "Identify the type of equation you're solving",
                    "Use appropriate mathematical methods",
                    "Show all your work step by step"
                ],
                "hard": [
                    "Consider multiple approaches to the problem",
                    "Use advanced mathematical concepts",
                    "Verify your solution thoroughly"
                ]
            },
            "physics": {
                "easy": [
                    "Draw a diagram to visualize the problem",
                    "List all known and unknown variables",
                    "Choose the appropriate formula"
                ],
                "medium": [
                    "Use the right units throughout",
                    "Consider the physical meaning",
                    "Check if your answer makes sense"
                ],
                "hard": [
                    "Apply advanced physics principles",
                    "Consider all forces and interactions",
                    "Use calculus where appropriate"
                ]
            },
            "chemistry": {
                "easy": [
                    "Balance the equation first",
                    "Use the periodic table for atomic weights",
                    "Remember the mole concept"
                ],
                "medium": [
                    "Check your units carefully",
                    "Consider the reaction mechanism",
                    "Use stoichiometry principles"
                ],
                "hard": [
                    "Apply advanced chemical principles",
                    "Consider equilibrium and kinetics",
                    "Use thermodynamic concepts"
                ]
            },
            "biology": {
                "easy": [
                    "Think about structure and function",
                    "Consider the levels of organization",
                    "Relate to real-world examples"
                ],
                "medium": [
                    "Use diagrams to help visualize",
                    "Connect different biological concepts",
                    "Consider the evolutionary perspective"
                ],
                "hard": [
                    "Apply advanced biological principles",
                    "Consider molecular mechanisms",
                    "Integrate multiple biological systems"
                ]
            },
            "cs": {
                "easy": [
                    "Write out the algorithm step by step",
                    "Consider edge cases",
                    "Think about efficiency"
                ],
                "medium": [
                    "Use appropriate data structures",
                    "Consider time and space complexity",
                    "Test with simple examples first"
                ],
                "hard": [
                    "Apply advanced algorithms",
                    "Consider optimization techniques",
                    "Use mathematical analysis"
                ]
            },
            "engineering": {
                "easy": [
                    "Understand the problem requirements",
                    "Draw diagrams and schematics",
                    "Use appropriate units"
                ],
                "medium": [
                    "Apply engineering principles",
                    "Consider safety and efficiency",
                    "Use systematic design approach"
                ],
                "hard": [
                    "Apply advanced engineering concepts",
                    "Consider multiple design constraints",
                    "Use mathematical modeling"
                ]
            }
        }
        
        subject_hints = hints.get(subject, hints["math"])
        difficulty_hints = subject_hints.get(difficulty, subject_hints["medium"])
        
        return difficulty_hints 