import os

import cv2
import numpy as np
from cnocr import CnOcr

import config
from logs import logger

ocr = CnOcr(rec_model_name=config.rec_model_name,
            det_model_name=config.det_model_name,
            rec_root=os.path.join(config.model_dir, 'cnocr'),
            det_root=os.path.join(config.model_dir, 'cnstd'))


def match_template(image: np.ndarray, template: np.ndarray) -> dict:
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    box = tuple(max_loc) + tuple(map(sum, zip(template.shape, max_loc)))
    logger.debug('match template at {0} with score: {1}'.format(max_val, box))
    return {'val': max_val, 'box': box}


def _ocr_image(image: np.ndarray) -> dict:
    results = ocr.ocr(image)
    data_dict = {}
    for result in results:
        box = tuple(np.hstack(result['position'].astype(int)[[0, 2]]))
        logger.debug('find {0} at {1} with score: {2}'.format(result['text'], box, result['score']))
        data_dict[result['text']] = {'val': result['score'], 'box': box}
    return data_dict


def ocr_image_text(image: np.ndarray, text: str) -> dict:
    data_dict = _ocr_image(image)
    if text == '':
        error_str = 'can not input no text in ocr_image_text'
        logger.error(error_str)
        raise ValueError(error_str)
    if text not in data_dict.keys():
        info_str = 'text {0} not find'.format(text)
        logger.info(info_str)
        raise UserWarning(info_str)
    data = data_dict[text]
    logger.debug('match text {0} at {1} with score: {2}'.format(text, data_dict['val'], data_dict['box']))
    return data
