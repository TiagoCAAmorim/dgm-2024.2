# PATHS
PATH_TRAIN = "data/coco/train" # data/city/train, data/coco/train
PATH_TEST = "data/coco/val" # data/city/val, data/coco/val
PATH_MODELS = "models/"
PATH_FIGS = "figs/"
RUN_ID = "COCO-GC_240-4-10-MSE_03-03-300_PT"

# ARCHITECTURE
C_MODE = 0 # 0=GC, 1=GC+, 2=SC
DEVICE = 'cuda'
## COMPLEXITY
FILTERS = 240 # 64, 128, 240, 480
N_BLOCKS = 6 # 4, 5, 6, 7
CHANNELS = 4 # 2, 4, 8
N_CONVS = 4
LAMBDA_D = 10
GAN_LOSS = "MSE" # BCE, MSE
## DATA
CROP_SHAPE = (384, 384) # CITY: (384, 768); COCO: (384, 384)
SHORT_SIZE = 192 # CITY: 96, 128, 192; COCO: 128, 192, 256
## EXTRA TECHNIQUES
DROPOUT = 0.0 # 0, 0.3
REAL_LABEL = 1.0
FAKE_LABEL = 0.0
INPUT_NOISE = 0.0 # 0.0, 0.1
## QUANTIZER
SIGMA = 1000.
LEVELS = 8
L_MIN = -2.1
L_MAX = 2.1

# TRAINING
OPTIMIZER_BETAS = (0.5, 0.999)
AE_LR = 3E-4 # 1E-4, 3E-4, 1E-3
DC_LR = 3E-4 # 1E-4, 3E-4, 1E-3
BATCH_SIZE = 300 # CITY: 50, 100, 150; COCO: 100, 200, 300
PT_EPOCHS = 40 # 0, 40
FT_EPOCHS = 40 # 1, 10, 40, 80

# TRACKING
PLOT_EVERY = 10
SAVE_EVERY = 20
