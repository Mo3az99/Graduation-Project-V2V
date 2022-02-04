import numpy as np


class bcnSample(object):
    def __init__(self, bEncrypted, vehId=0, psym=0, timestamp=0) -> None:
        super().__init__()
        self.bEncrypt = bEncrypted
        self.vehId = vehId
        self.psym = psym
        self.timestamp = timestamp
        self.px
        self.vx
        self.py
        self.vy
        self.angle


#class KalmanTrack(object):
#    pass


class kalmanTrack(object):
    p0 = 50
    q = 0.7
    rp = 5
    rv = 2
    bcnT = 1
    lastTrackdId = 0
    bKalmanParamInitialized = False

    def __init__(self) -> None:
        super().__init__()
        self.id = -1
        self.bActive = True
        self.lifeTime = 0
        self.lastUpdateTime = -1
        self.vehId
        self.pseudonym

        # somestuff should be here MatrixXd H, F, P, Q, S, R, K, Sinv;

        self.P = np.zeros((3, 3))
        self.P[0.0] = self.p0;

        self.F = np.ones((3, 3))
        self.F[0, 1] = self.bcnT
        self.F[0, 2] = (self.bcnT * self.bcnT) / 2
        self.F[1, 2] = self.bcnT

        self.H = np.ones((2, 3))

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
        self.S = self.H * self.P * (self.H.transpose()) + self.R

        self.Sinv = np.zeros((2, 2))
        self.Sinv = np.linalg.inv(self.S)

        self.Sdev = np.linalg.det(self.S)

        self.K = np.zeros((3, 2))

    def __init__(self, bcn: bcnSample, tm) -> None:
        super().__init__()
        self.__init__(self)
        self.lastUpdateTime = tm
        kalmanTrack.lastTrackId += 1
        self.id = kalmanTrack.lastTrackedId
        self.vehId = bcn.vehId
        self.pseudonym = bcn.psym
        self.lifeTime = 1
        self.x[0] = (bcn.px)
        self.x[1] = (bcn.vx)
        self.x[2] = (bcn.py)
        self.x[3] = (bcn.vx)

    def predict(self) -> None:
        temp = np.zeros((3, 1))
        temp = self.F * self.X
        self.x[0] = temp[0]
        self.x[1] = temp[1]
        self.x[2] = temp[2]
        self.x[3] = temp[6]
        self.x[4] = temp[7]
        self.x[5] = temp[8]

        self.P = self.F * self.P * self.F.transpose() + self.Q

    def clacD(self, bcn: bcnSample) -> float:
        temp = np.zeros(2)
        Hx = np.zeros(4)
        z = np.zeros(4)
        y = np.zeros(4)
        tmp = np.zeros(1)

        temp = self.H * self.X

        Hx[0] = temp[0]
        Hx[1] = temp[1]
        Hx[2] = temp[7]
        Hx[3] = temp[8]

        z = np.array([bcn.px, bcn.vx, bcn.py, bcn.vy])

        y = z - Hx

        to7atmp1 = np.array([y[0], y[1]])
        to7atmp2 = np.array([y[2], y[3]])

        tmp = (to7atmp1.transpose() * self.Sinv) * to7atmp1 + (to7atmp2.transpose() * self.Sinv) * to7atmp2
        tmp = tmp ** 2
        return tmp


    def update(self, z: bcnSample, tm) -> None:
        zVec = np.zeros((2, 1))
        self.vehId = z.vehId
        self.pseudonym = z.psym
        self.lifeTime += 1
        self.bActive = True
        self.lastUpdateTime = tm

        I = np.ones((2, 2))
        ik = np.zeros((3, 3))
        x_prior = np.zeros(6)
        p_prior = np.zeros(6)

        x_prior = self.X
        p_prior = self.Y

        self.S = self.H * p_prior * self.H.transpose() + self.R
        self.Sinv = np.linalg.inv(self.S)
        self.Sdet = np.linalg.det(self.S)

        self.K = p_prior * self.H.transpose() * self.Sinv

        to7atmp1 = np.array([x_prior[0], x_prior[1], x_prior[2]])
        to7atmp2 = np.array([x_prior[6], x_prior[7], x_prior[8]])

        zVec = np.array([z.px, z.py])

        temp = to7atmp1 + self.K * (zVec - self.H * to7atmp1)
        self.X[0] = temp[0]
        self.X[1] = temp[1]
        self.X[2] = temp[2]

        zVec = np.array([z.py, z.vy]) #momkn deh 8alat

        temp = to7atmp2 + self.K * (zVec - self.H * to7atmp2)

        self.X[3] = temp[0]
        self.x[4] = temp[1]
        self.X[5] = temp[2]

        ik = np.ones((np.shape(self.K[0], np.shape(self.K[1]) - (self.K * self.H))))

        self.P = ik * p_prior * ik.transpose() + self.K * self.R * self.K.transpose()








