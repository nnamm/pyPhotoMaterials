"""Scripts for note publication

Create the photo material data for note publication. The data file is zip based on the
jpg files output from Lightroom Classic.

"""

import logging
import re
import sys
import zipfile
from pathlib import Path
from typing import Dict
from typing import List

import settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class PhotoMaterials(object):
    """Photo Material class"""

    def __init__(self, image_sizes: List[str]):
        self.image_sizes = image_sizes

    def get_file_lists(self) -> Dict[str, List[str]]:
        """Get file lists function.

        Set the dictionary data from working dir.

        Returns:
            temp_dict:
                File lists.
                The key is the image size, the value is its file list.

        """

        temp_dict = {}
        work_path = Path(settings.photo_work_dir)
        for size in self.image_sizes:
            temp_list = [
                file.name
                for file in work_path.iterdir()
                if file.suffix == ".jpg" and size in file.name
            ]
            temp_dict[size] = sorted(temp_list)
        return temp_dict

    @staticmethod
    def get_material_number(re_target_list: List[str]) -> str:
        """Get material number function.

        Set the photo material number from a file name.
        (ex. when file name is 'No10-S-01.jpg', materials number is '10'.)

        Args:
            re_target_list: A list of files used in the search.

        Returns:
            temp_num: Material number.

        """

        temp_num = ""
        num_from_filename = re.search(r"\d+", re_target_list[0])
        if not num_from_filename:
            logger.error(
                {
                    "action": "get_material_number",
                    "error": "file error: " + re_target_list[0],
                }
            )
            return temp_num
        temp_num = num_from_filename.group()
        return temp_num

    def create_zip_file(
        self, file_lists_dict: Dict[str, List[str]], material_num: str
    ) -> None:
        """Create zip files function.

        Create ZIP files using the file list(dict) of the arguments.
        The ZIP file name is determined by the JPG file name and image size.

        Args:
            file_lists_dict:
                Dictionary with the image size as key and the file lists as value.
            material_num:
                Photo materials number.

        Returns:
            None.

        """

        for size in self.image_sizes:
            zip_name = f"No{material_num}-{size}.zip"
            logger.info(
                {"action": "create_zip_file", "message": "Creation start: " + zip_name}
            )

            with zipfile.ZipFile(
                settings.photo_work_dir + zip_name,
                "w",
                compression=zipfile.ZIP_DEFLATED,
            ) as new_zip:
                for file in file_lists_dict[size]:
                    new_zip.write(settings.photo_work_dir + f"{file}", arcname=file)
                    logger.info(
                        {
                            "action": "create_zip_file",
                            "message": "Combining...: " + file,
                        }
                    )
            logger.info({"action": "create_zip_file", "message": "Creation finish"})

        logger.info({"action": "create_zip_file", "message": "Creation completed"})
