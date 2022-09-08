import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Wrapper of count the function execution time
def timeCount(func):
    def wrapper(*args, **kwargs):
        print(f" STEP (RUN ) :  {func.__name__}", end="\r")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f" STEP (Done)\t\t\t-> {end - start :5.2f} s \u2713")
        return result

    return wrapper


# Extract the data
class Extractor(object):
    def __init__(self, data) -> None:
        self.database = data.get_database()
        self.column = data.get_columns()
        self.lag_number = len(self.database)

    @timeCount
    def get_position_db(self, type_: int, pos_: list[str] = ["x", "y", "z"]):
        db_position = []
        for idx in range(self.lag_number):
            df_data = pd.DataFrame(data=self.database[idx], columns=self.column)
            df_one = df_data[df_data["type"] == type_]
            unit_position = df_one[pos_]
            db_position.append(unit_position)
        return np.array(db_position)


# Linear Regression
class LinearRegression:
    def __init__(self, eta=0.01, n_iter=10000, random_state=1) -> None:
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    @timeCount
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Do Linear Regression

        y = w_[0] * x + w_[1]

        Args:
            X (np.ndarray): x data
            y (np.ndarray): y data
        """
        self.X = X.reshape(-1, 1)
        self.y = y.reshape(-1, 1)
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=(2, 1))
        # self.w_ = np.array([[0.2],[0]])
        self.n = len(X)
        self.costs_ = []
        self.steps_ = []

        for step in range(self.n_iter):
            self.costs_.append(self.cost())
            self.update_w_()
            self.steps_.append(step)

            # if self.costs_[-1] <= 1e-6:
            #     print(1)
            #     break

        self.plot_cost_and_data()

    def cost(self):
        cost = np.dot(
            1 / (2 * self.n), np.sum(np.square(np.subtract(self.hypothesis(), self.y)))
        )
        return cost

    def update_w_(self):
        w_gradient = (
            self.eta / self.n * np.dot(np.subtract(self.hypothesis(), self.y).T, self.X)
        )
        b_gradient = self.eta / self.n * np.sum(np.subtract(self.hypothesis(), self.y))
        self.w_[0] = np.subtract(self.w_[0], w_gradient)
        self.w_[1] = np.subtract(self.w_[1], b_gradient)

    def hypothesis(self):
        return np.add(np.dot(self.X, self.w_[0:1]), self.w_[1])

    def plot_cost_and_data(self):
        fig, axs = plt.subplots(1, 2, constrained_layout=True)
        fig.tight_layout()
        # Cost Function
        axs[0].loglog(self.steps_, self.costs_, "ko-")
        axs[0].set_xlabel("step (log)")
        axs[0].set_ylabel("cost (log) ")
        # Main Function
        axs[1].plot(self.X, self.hypothesis(), color="black")
        axs[1].scatter(self.X, self.y, color="red", alpha=0.10)
        axs[1].set_xlabel("X")
        axs[1].set_ylabel("Y")
