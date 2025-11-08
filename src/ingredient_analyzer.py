"""
Ingredient Analyzer using OpenAI API
Analyzes ingredients for health impact, allergens, and certifications.
"""

import os
import json
from typing import Dict, Optional, List
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class IngredientAnalyzer:
    """Analyzes ingredients using OpenAI API for health and safety insights."""
    
    SYSTEM_PROMPT = """You are an AI nutrition and cosmetic safety assistant with expertise in:
- Food safety regulations (FDA, EFSA, etc.)
- Cosmetic ingredient safety (INCI, EU Cosmetics Regulation)
- Allergen identification
- Health impact assessment
- Product certifications (Halal, Vegan, Organic, etc.)

Your role is to analyze ingredient lists and provide factual, evidence-based health and safety information.
Always base your analysis on scientific consensus and regulatory guidelines.
Be objective and avoid exaggeration - provide balanced assessments.
"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the analyzer.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.client = OpenAI(api_key=self.api_key)
    
    def _create_analysis_prompt(
        self,
        product_type: str,
        ingredients_text: str,
        expiration_date: Optional[str] = None
    ) -> str:
        """
        Create the analysis prompt for OpenAI.
        
        Args:
            product_type: Type of product (food/drink/beauty)
            ingredients_text: Ingredients list text
            expiration_date: Expiration date if available
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Analyze the following {product_type} product ingredients:

INGREDIENTS: {ingredients_text}
"""
        
        if expiration_date:
            prompt += f"\nEXPIRATION DATE: {expiration_date}\n"
        
        prompt += """
Please provide a comprehensive analysis in the following JSON format:

{
  "harmful_ingredients": [],          // Ingredients with known health risks
  "additives": [],                    // Food/cosmetic additives (E-numbers, etc.)
  "preservatives": [],                // Preservatives identified
  "irritants": [],                    // Potential skin/eye irritants (for beauty products)
  "allergens": [],                    // Common allergens (FDA top 9, EU top 14, etc.)
  "chemicals": [],                    // Notable chemical compounds
  "certifications": [],               // Likely certifications (Halal, Vegan, Gluten-Free, etc.)
  "fda_approval": "Likely/Unverified/Not Found",  // FDA/regulatory approval status
  "healthiness_rating": 0,            // Scale 1-10 (1=very unhealthy, 10=very healthy)
  "expiration_valid": true,           // Is product still safe to use? (if date provided)
  "recommendation": "",               // Brief recommendation (1-2 sentences)
  "health_suggestion": ""             // Personalized health tip (1-2 sentences)
}

Important guidelines:
- Only list ingredients that are actually present
- Be specific about why something is harmful/beneficial
- Base ratings on scientific evidence
- For allergens, include both obvious and hidden sources
- For certifications, only suggest those likely based on ingredients
- Be conservative with the healthiness rating
- Consider the product type in your analysis
"""
        
        return prompt
    
    def analyze(
        self,
        product_type: str,
        ingredients_text: str,
        expiration_date: Optional[str] = None,
        manufacture_date: Optional[str] = None
    ) -> Dict:
        """
        Analyze ingredients using OpenAI API.
        
        Args:
            product_type: Type of product (food/drink/beauty)
            ingredients_text: Ingredients list text
            expiration_date: Expiration date if available
            manufacture_date: Manufacture date if available
            
        Returns:
            Structured analysis results
        """
        if not ingredients_text:
            return {
                'success': False,
                'error': 'No ingredients text provided'
            }
        
        try:
            # Check expiration validity
            expiration_valid = self._check_expiration_validity(expiration_date)
            
            # Create prompt
            prompt = self._create_analysis_prompt(
                product_type,
                ingredients_text,
                expiration_date
            )
            
            # Call OpenAI API with structured output
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=2000
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Override expiration_valid with our calculation
            result['expiration_valid'] = expiration_valid
            
            # Add metadata
            result['success'] = True
            result['model_used'] = self.model
            result['analysis_date'] = datetime.now().isoformat()
            
            return result
        
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Failed to parse OpenAI response: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Analysis failed: {str(e)}'
            }
    
    def _check_expiration_validity(self, expiration_date: Optional[str]) -> bool:
        """
        Check if product is still valid based on expiration date.
        
        Args:
            expiration_date: Expiration date string (YYYY-MM-DD)
            
        Returns:
            True if valid/unknown, False if expired
        """
        if not expiration_date:
            return True  # Unknown, assume valid
        
        try:
            exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            current_date = datetime.now()
            return exp_date >= current_date
        except:
            return True  # If parsing fails, assume valid
    
    def quick_analysis(self, ingredients_text: str) -> Dict:
        """
        Simplified analysis without product type classification.
        
        Args:
            ingredients_text: Ingredients list text
            
        Returns:
            Analysis results
        """
        return self.analyze(
            product_type='general',
            ingredients_text=ingredients_text
        )


if __name__ == "__main__":
    # Test the analyzer
    analyzer = IngredientAnalyzer()
    
    test_ingredients = "Water, Sugar, Citric Acid, Sodium Benzoate, Artificial Flavor, Yellow 5"
    result = analyzer.analyze(
        product_type='drink',
        ingredients_text=test_ingredients,
        expiration_date='2026-12-31'
    )
    
    print(json.dumps(result, indent=2))
