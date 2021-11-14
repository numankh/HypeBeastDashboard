import spacy
from textstat.textstat import textstatistics,legacy_round
import textstat
import en_core_web_sm

# While the maximum score is 121.22, there is no limit on how low the score can be. A negative score is valid.
def flesch_reading_ease_score(text):
	return textstat.flesch_reading_ease(text)

# Average of all grade level readability indices 
def average_grade_score(text):
	total = textstat.flesch_kincaid_grade(text) + textstat.gunning_fog(text) + textstat.automated_readability_index(text) + textstat.coleman_liau_index(text) + textstat.linsear_write_formula(text) + textstat.dale_chall_readability_score(text)
	return round(total / 6, 2)

if __name__ == "__main__":
    sample_text = "I dont understand what is going on please work my name is numan khan "
    print(textstat.flesch_reading_ease(sample_text))
    print(average_grade_score(sample_text))