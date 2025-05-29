import pickle
#from tensorflow.keras.models import save_model  # Correct import

# Load the pickled Keras model
with open(r'c:\Users\USER\Downloads\model.pkl', 'rb') as f:
    model = pickle.load(f)

# Save as .h5 format
#ave_model(model, 'model_converted.h5')
