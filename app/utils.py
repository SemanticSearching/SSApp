"""
utils
"""
from sentence_transformers import SentenceTransformer
import pickle
import faiss
from faiss import normalize_L2
import numpy as np

ALLOWED_EXTENSIONS = {'docx', 'pdf', 'doc'}


def load_bert_model(name="distilbert-base-nli-stsb-mean-tokens"):
    """Instantiate a sentence-level DistilBERT model."""
    return SentenceTransformer(name)


def load_faiss_index(path_to_faiss):
    """Load and deserialize the Faiss index."""
    with open(path_to_faiss, "rb") as h:
        data = pickle.load(h)
    return faiss.deserialize_index(data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def vector_search(query, model, index, num_results=10, threshold=0.75):
    """Tranforms query to vector using a pretrained, sentence-level
    DistilBERT model and finds similar vectors using FAISS.
    Args:
        query (str): User query that should be more than a sentence long.
        model (sentence_transformers.SentenceTransformer.SentenceTransformer)
        index (`numpy.ndarray`): FAISS index that needs to be deserialized.
        num_results (int): Number of results to return.
        threshold: filter the D and I
    Returns:
        D (:obj:`numpy.array` of `float`): Distance between results and query.
        I (:obj:`numpy.array` of `int`): Paper ID of the results.

    """
    vector = model.encode(list(query))
    normalize_L2(vector)
    D, I = index.search(np.array(vector).astype("float32"), k=num_results)
    index = I.flatten()
    distance = D.flatten()
    filter = distance > threshold
    if distance[filter].tolist():
        pass
    else:
        index = index[:3]
        distance = distance[:3]
        filter = distance > threshold/2
    return distance[filter].tolist(), index[filter].tolist()

