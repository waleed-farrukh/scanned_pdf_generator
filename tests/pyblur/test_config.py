import os
import json
import pathlib

def config_path_decide():
    if(pathlib.Path().resolve().name == 'pyblur'):
        config_path = pathlib.Path('resources').resolve() / ('config.json')
    else:
        config_path = pathlib.Path('pyblur/resources').resolve() / ('config.json')
    return config_path


def test_config():
    config_path = config_path_decide()
    if(not os.path.exists(config_path)):
        "Error loading config file. Make sure config exists"


def test_dpi():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert data["dpi"] == 300, "DPI should be equal to 300"


def test_motion_blur():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'motion_blur' in data, "Motion Blur does not exist"
    param = data['motion_blur']
    if(not param['apply']):
        "Motion Blur parameter apply failed"
    assert param['dim'] == [3, 5, 7], "Motion Blur parameter dim failed"
    assert param['angle_start'] == 90,\
        "Motion Blur parameter angle_start failed"
    assert param['angle_end'] == 150, "Motion Blur parameter angle_end failed"
    assert param['angle_step'] == 5, "Motion Blur parameter angle_step failed"
    assert param['linetype'] == ['full', 'left', 'right'], \
        "Motion Blur parameter linetype failed"


def test_gaussian_blur():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'gaussian_blur' in data, "Gaussian Blur does not exist"
    param = data['gaussian_blur']
    if(not param['apply']):
        "Gaussian Blur parameter apply failed"
    assert param['kernel_start'] == 1, \
        "Gaussian Blur parameter kernel_start failed. Must be 1"
    assert param['kernel_end'] == 5, \
        "Gaussian Blur parameter kernel_end failed"
    assert param['sigma_x_start'] == 0, \
        "Gaussian Blur parameter sigma_x_start failed"
    assert param['sigma_x_end'] == 3, \
        "Gaussian Blur parameter sigma_x_end failed"
    assert param['sigma_y_start'] == 0, \
        "Gaussian Blur parameter sigma_y_start failed"
    assert param['sigma_y_end'] == 3, \
        "Gaussian Blur parameter sigma_y_end failed"


def test_focus_blur():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'focus_blur' in data, "Focus Blur does not exist"
    param = data['focus_blur']
    if(not param['apply']):
        "Focus Blur parameter apply failed"
    assert param['dim'] == [3, 5, 7, 9], "Focus Blur parameter dim failed "


def test_psf_blur():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'psf_blur' in data, "PSF Blur does not exist"
    param = data['psf_blur']
    if(not param['apply']):
        "PSF Blur parameter apply failed"
    assert param['psf_id_start'] == 1, "PSF Blur parameter psf_id_start failed"
    assert param['psf_id_end'] == 20, "PSF Blur parameter psf_id_end failed"
    assert param['psf_id_step'] == 5, "PSF Blur parameter psf_id_step failed"


def test_gamma():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'gamma' in data, "Gamma does not exist"
    param = data['gamma']
    if(not param['apply']):
        "Gamma parameter apply failed"
    assert param['gamma_start'] == 0.1, "Gamma parameter gamma_start failed"
    assert param['gamma_end'] == 2.0, "Gamma parameter gamma_end failed"
    assert param['gamma_step'] == 0.1, "Gamma parameter gamma_step failed"


def test_brightness_change():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'brightness_change' in data, 'Brightness Change does not exist'
    param = data['brightness_change']
    if(not param['apply']):
        "Brightness Change parameter apply failed"
    assert param['brightness_change_start'] == -50, \
        "Brightness Change parameter brightness_change_start failed"
    assert param['brightness_change_end'] == 30, \
        "Brightness Change parameter brightness_change_end failed"
    assert param['brightness_change_step'] == 5, \
        "Brightness Change parameter brightness_change_step failed"


def test_gamma_spatial():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'gamma_spatial' in data, "Gamma Spatial does not exist"
    param = data['gamma_spatial']
    if(not param['apply']):
        "Gamma Spatial parameter apply failed"
    assert param['gamma_start'] == 0.3, \
        "Gamma Spatial parameter gamma_start failed"
    assert param['gamma_end'] == 1.7, \
        "Gamma Spatial parameter gamma_end failed"
    assert param['gamma_step'] == 0.1, \
        "Gamma Spatial parameter gamma_step failed"
    assert param['x_start'] == 0.35, \
        "Gamma Spatial parameter x_start failed"
    assert param['x_end'] == 0.7, \
        "Gamma Spatial parameter x_end failed"
    assert param['x_step'] == 0.05, \
        "Gamma Spatial parameter x_step failed"
    assert param['y_start'] == 0.35, \
        "Gamma Spatial parameter y_start failed"
    assert param['y_end'] == 0.7, \
        "Gamma Spatial parameter y_end failed"
    assert param['y_step'] == 0.05, \
        "Gamma Spatial parameter y_step failed"


def test_salt_pepper():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'salt_pepper' in data, \
        "Salt Pepper does not exist"
    param = data['salt_pepper']
    if(not param['apply']):
        "Salt Pepper parameter apply failed"
    assert param['salt_start'] == 0.0, \
        "Salt Pepper parameter salt_start failed"
    assert param['salt_end'] == 0.0001, \
        "Salt Pepper parameter salt_end failed"
    assert param['salt_step'] == 5e-06, \
        "Salt Pepper parameter salt_step failed"
    assert param['pepper_start'] == 0.0, \
        "Salt Pepper parameter pepper_start failed"
    assert param['pepper_end'] == 0.0001, \
        "Salt Pepper parameter pepper_end failed"
    assert param['pepper_step'] == 5e-06, \
        "Salt Pepper parameter pepper_step failed"


def test_rotation():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'rotation' in data, \
        "Rotation does not exist"
    param = data['rotation']
    if(not param['apply']):
        "Rotation parameter apply failed"
    assert param['rotation_angle_start'] == -3, \
        "Rotation parameter rotation_angle_start failed"
    assert param['rotation_angle_end'] == 3, \
        "Rotation parameter rotation_angle_end failed"
    assert param['rotation_angle_step'] == 0.5, \
        "Rotation parameter rotation_angle_step failed"


def test_perspective():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'perspective' in data, \
        "Perspective does not exist"
    param = data['perspective']
    if(not param['apply']):
        "Perspective parameter apply failed"
    assert param['perspective_x_start'] == -3e-05, \
        "Perspective parameter perspective_x_start failed"
    assert param['perspective_x_end'] == 8e-06, \
        "Perspective parameter perspective_x_end failed"
    assert param['perspective_y_start'] == -3e-05, \
        "Perspective parameter perspective_y_start failed"
    assert param['perspective_y_end'] == 8e-06, \
        "Perspective parameter perspective_y_end failed"


def test_background():
    config_path = config_path_decide()
    with open(config_path, 'r') as json_str:
        data = json.load(json_str)
    assert 'background' in data, "Background does not exist"
    param = data['background']
    if(not param['apply']):
        "Background parameter apply failed"
    assert param['zoom'] == 0.01, "Background parameter zoom failed"
