from .__init__ import *
from .tools import timeCount

# Linear Regression
class LinearRegression:
    def __init__(self, eta=0.01, n_iter=10000, random_state=1) -> None:
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    @timeCount
    def fit(self, X: NDArray, y: NDArray):
        """Do Linear Regression

        y = w_[0] * x + w_[1]

        Args:
            X (NDArray): x data
            y (NDArray): y data
        """
        self.X = X.reshape(-1, 1)
        self.y = y.reshape(-1, 1)
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=(2, 1))
        self.n = len(X)
        self.costs_ = []
        self.steps_ = []

        for step in range(self.n_iter):
            self.costs_.append(self.cost())
            self.update_w_()
            self.steps_.append(step)
        self.plot_cost_and_data()

    def cost(self):
        cost = np.dot(1 / (2 * self.n), np.sum(np.square(np.subtract(self.hypothesis(), self.y))))
        return cost

    def update_w_(self):
        w_gradient = self.eta / self.n * np.dot(np.subtract(self.hypothesis(), self.y).T, self.X)
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
