import logging
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IntroAnalyzer:
    def __init__(self):
        pass

    def analyze_expressions(self, expressions_data):
        """Analyze preprocessed facial expression data"""
        if not expressions_data:
            return {}
            
        # Filter out None values
        valid_expressions = [exp for exp in expressions_data if exp is not None]
        
        if not valid_expressions:
            return {}

        # Calculate average expression values
        total_neutral = sum(exp.get('neutral', 0) for exp in valid_expressions)
        total_happy = sum(exp.get('happy', 0) for exp in valid_expressions)
        count = len(valid_expressions)

        expression_percentages = {
            'neutral': (total_neutral / count) * 100,
            'happy': (total_happy / count) * 100
        }

        return expression_percentages

    def analyze_eye_contact(self, eye_contact_data):
        """Analyze preprocessed eye contact data"""
        if not eye_contact_data or len(eye_contact_data) == 0:
            return 0

        data = eye_contact_data[0]  # Assuming single entry with totals
        total_frames = data.get('total', 0)
        true_count = data.get('trueCount', 0)

        if total_frames == 0:
            return 0

        return (true_count / total_frames) * 100

    def analyze_text(self,video_length, text):
        """Analyze transcript text for sentiment"""
        if not text:
            return None, None, 0

        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            word_count = len(blob.words)
            speaking_rate = word_count/video_length  

            return sentiment, speaking_rate, word_count
        except Exception as e:
            logging.error(f"Error analyzing text: {e}")
            return None, None, 0

    def calculate_confidence_score(self, expression_percentages, eye_contact_percentage, sentiment=None, speaking_rate=None):
        """Calculate overall confidence score"""
        if not expression_percentages:
            return None

        if sentiment is not None and speaking_rate is not None:
            confidence_score = (
                eye_contact_percentage * 0.3 +
                expression_percentages.get('happy', 0) * 0.2 +
                expression_percentages.get('neutral', 0) * 0.15 +
                (sentiment + 1) * 50 * 0.2 +
                min(speaking_rate / 150 * 100, 100) * 0.15
            )
        else:
            confidence_score = (
                eye_contact_percentage * 0.4 +
                expression_percentages.get('happy', 0) * 0.3 +
                expression_percentages.get('neutral', 0) * 0.3
            )

        return confidence_score

    def analyze(self, expressions_data, eye_contact_data,video_length, transcript_text=""):
        """Main analysis method"""
        # Analyze facial expressions
        expression_percentages = self.analyze_expressions(expressions_data)
        
        # Analyze eye contact
        eye_contact_percentage = self.analyze_eye_contact(eye_contact_data)
        
        # Analyze text if provided
        sentiment, speaking_rate, word_count = self.analyze_text(video_length,transcript_text)
        
        # Calculate confidence score
        confidence_score = self.calculate_confidence_score(
            expression_percentages,
            eye_contact_percentage,
            sentiment,
            speaking_rate
        )

        return {
            "facial_expressions": expression_percentages,
            "eye_contact": eye_contact_percentage,
            "speech_sentiment": sentiment,
            "speaking_rate": speaking_rate,
            "word_count": word_count,
            "confidence_score": confidence_score
        }


