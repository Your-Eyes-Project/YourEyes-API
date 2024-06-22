from transformers import pipeline

def load_model():
    return pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v1")

def find_closest_classes(user_question, model, class_names):
    output = model(user_question, class_names, multi_label=False)
    print(f"user question: {output['sequence']}\n objects to detect: {output['labels'][0]}")
    word= output['labels'][0]
    object=[class_names.index(word)]
    return object
