from src.utils.token_estimator import TokenEstimator

text = "Hello world!"

tokens = TokenEstimator.estimate(text)

print(tokens)

assert tokens > 0

print("TokenEstimator test passed!")