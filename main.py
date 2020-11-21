"""Scripts for note publication

This is main controller.

"""

import logging
import sys

import settings
from material import PhotoMaterials
from publish import Publish

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def main():
    """Main process"""

    # Create
    pm_cls = PhotoMaterials(settings.image_sizes)
    file_lists_dict = pm_cls.get_file_lists()
    material_num = pm_cls.get_material_number(file_lists_dict[settings.image_sizes[0]])
    pm_cls.create_zip_file(file_lists_dict, material_num)

    # Publish
    ph_cls = Publish(settings.image_sizes, file_lists_dict, material_num)
    if ph_cls.upload_file():
        ph_cls.create_url_text()


if __name__ == "__main__":
    main()
