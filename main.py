""" Main Python file to start routines """

from argparse import ArgumentParser
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import LearningRateLogger, EarlyStopping, ModelCheckpoint
from pytorch_lightning.callbacks import model_checkpoint
from model import LightningModel
from data import SpyGlassDataModule, Dataset2DGenerator
from config import Config


# +-------------------------------------------------------------------------------------+ #
# |                                                                                     | #
# |                                          INIT                                       | #
# |                                                                                     | #
# +-------------------------------------------------------------------------------------+ #

def init_data(input_root, medical_data_csv_path=None):
    return SpyGlassDataModule(input_root, medical_data_csv_path)

def init_model():
    return LightningModel()

def init_trainer():
    """ Init a Lightning Trainer using from_argparse_args
    Thus every CLI command (--gpus, distributed_backend, ...) become available.
    """
    parser = ArgumentParser()
    parser = Trainer.add_argparse_args(parser)
    args   = parser.parse_args()
    lr_logger      = LearningRateLogger()
    early_stopping = EarlyStopping(monitor='val_loss', mode='min', min_delta=0.001, patience=5, verbose=True)
    return Trainer.from_argparse_args(args, callbacks = [lr_logger, early_stopping])




# +-------------------------------------------------------------------------------------+ #
# |                                                                                     | #
# |                                          RUN                                        | #
# |                                                                                     | #
# +-------------------------------------------------------------------------------------+ #

def make_2d_dataset(video_root, output_root, sampling_factor, crop):
    dataset_generator = Dataset2DGenerator(video_root, output_root, sampling_factor, crop)
    dataset_generator.run()

def run_training(input_root, medical_data_csv_path):
    """ Instanciate a datamodule, a model and a trainer and run trainer.fit(model, data) """
    data   = init_data(input_root, medical_data_csv_path)
    model, trainer = init_model(), init_trainer()
    trainer.fit(model, data)

def test(input_root, model_path):
    data    = init_data(input_root)
    model   = LightningModel.load_from_checkpoint(model_path)
    trainer = init_trainer()
    trainer.test()


if __name__ == '__main__':
    cfg = Config()
    # make_2d_dataset(cfg.video_root, cfg.data_2d_root, cfg.sampling_factor, cfg.crop)
    run_training(cfg.data_2d_root, cfg.medical_data_csv_path)
    # test('./lightning_logs/version_') 
