import numpy as np

#Kalman Classes
class bcnSample(object):
    def __init__(self, vehId, timestamp, px, py, vx, vy) -> None:
        super().__init__()
        # self.bEncrypt = bEncrypted
        self.vehId = vehId
        # self.psym = psym # id for car bet8yr
        self.timestamp = timestamp
        self.px = px
        self.vx = vx
        self.py = py
        self.vy = vy
        # self.angle

class kalmanTrack(object):
    p0 = 50
    q = 0.7
    rp = 5
    rv = 2
    bcnT = 1
    lastTrackId = 0
    bKalmanParamInitialized = False

    def zeroo(self):
        self.id = -1
        self.bActive = True
        self.lifeTime = 0
        self.lastUpdateTime = -1
        self.vehId = 0
        # self.pseudonym

        # somestuff should be here MatrixXd H, F, P, Q, S, R, K, Sinv;

        self.P = np.zeros((3, 3))
        self.P[0, 0] = self.p0

        self.F = np.identity(3)
        self.F[0, 1] = self.bcnT
        self.F[0, 2] = (self.bcnT * self.bcnT) / 2
        self.F[1, 2] = self.bcnT

        self.H = np.eye(2,M = 3)

        self.Q = np.zeros((3, 3))
        self.Q = np.array([[(self.bcnT ** 4) / 4, (self.bcnT ** 3) / 3, (self.bcnT ** 2) / 2],
                           [(self.bcnT ** 3) / 2, (self.bcnT ** 2), self.bcnT],
                           [(self.bcnT ** 2) / 2, self.bcnT, 1]])
        self.Q * self.q

        self.R = np.zeros((2, 2))
        self.R = np.array([[self.rp, 0],
                           [0, self.rv]])

        self.X = np.zeros(6)

        self.S = np.zeros((2, 2))
        #self.S = np.dot((np.dot(self.H, self.P)), (self.H.transpose())) + self.R
        self.S = np.dot(self.H, np.dot(self.P, self.H.transpose())) + self.R

        self.Sinv = np.zeros((2, 2))
        self.Sinv = np.linalg.inv(self.S)

        self.Sdev = np.linalg.det(self.S)

        self.K = np.zeros((3, 2))

    def __init__(self, bcn: bcnSample, tm) -> None:
        super().__init__()
        self.zeroo()
        self.lastUpdateTime = tm
        kalmanTrack.lastTrackId += 1
        self.id = kalmanTrack.lastTrackId
        self.vehId = bcn.vehId
        # self.pseudonym = bcn.
        self.lifeTime = 1
        self.X[0] = (bcn.px)
        self.X[1] = (bcn.vx)
        self.X[3] = (bcn.py)
        self.X[4] = (bcn.vx)

    def predict(self) -> None:
        tmpx = self.X[0:3]
        temp = np.dot(self.F, tmpx)
        self.X[0] = temp[0]
        self.X[1] = temp[1]
        self.X[2] = temp[2]
        tmpx = self.X[3:6]
        temp = np.dot(self.F, tmpx)
        self.X[3] = temp[0]
        self.X[4] = temp[1]
        self.X[5] = temp[2]
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q



    def update(self, z: bcnSample, tm) -> None:


        zVec = np.zeros((2, 1))
        self.vehId = z.vehId
        # self.pseudonym = z.psym
        self.lifeTime += 1
        self.bActive = True
        self.lastUpdateTime = tm

        x_prior = self.X
        p_prior = self.P

      #  self.S = np.dot((np.dot(self.H, p_prior)), (self.H.transpose())) + self.R
        self.S = self.R + np.dot(self.H, np.dot(p_prior, self.H.T))

        self.Sinv = np.linalg.inv(self.S)
        self.Sdet = np.linalg.det(self.S)

        self.K = np.dot((np.dot(p_prior, self.H.T)), self.Sinv)

        zVec = np.array([z.px, z.vx])

        temp = (x_prior[0:3]) + np.dot(self.K, zVec - np.dot(self.H, (x_prior[0:3])))

        self.X[0] = temp[0]
        self.X[1] = temp[1]
        self.X[2] = temp[2]

        zVec = np.array([z.py, z.vy])  # momkn deh 8alat

        temp = (x_prior[3:6]) + np.dot(self.K, zVec - np.dot(self.H, (x_prior[3:6])))

        self.X[3] = temp[0]
        self.X[4] = temp[1]
        self.X[5] = temp[2]

        ik = np.eye(len(self.K), M=len(self.K)) - np.dot(self.K, self.H)

        self.P = np.dot((np.dot(ik, p_prior)), ik.transpose()) + np.dot((np.dot(self.K, self.R)), self.K.transpose())
