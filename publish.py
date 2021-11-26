"""Scripts for note publication

Upload the photo material files for note publication. The target files are jpg/zip in a
given directory.

"""

import logging
import sys
from ftplib import FTP_TLS, all_errors
from pathlib import Path

import settings
import utils

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class Publish:
    """Publish class"""

    def __init__(
        self,
        image_sizes: list[str],
        file_lists_dict: dict[str, list[str]],
        material_num: str,
    ):
        self.image_sizes = image_sizes
        self.file_lists_dict = file_lists_dict
        self.material_num = material_num
        if settings.ftps_test_flag:
            self.ftps_upload_path = settings.ftps_test_path
        else:
            self.ftps_upload_path = settings.ftps_product_path

    def upload_file(self) -> bool:
        """Upload file function.

        Upload photo material files to server using FTP_TLS.

        Returns:
            bool: True if successful, False otherwise.

        """

        work_path = Path(settings.photo_work_dir)
        upload_list = [
            file for file in work_path.iterdir() if file.suffix in (".jpg", ".zip")
        ]

        with FTP_TLS(settings.ftps_host) as ftps:
            try:
                ftps.login(
                    settings.ftps_user,
                    settings.ftps_passwd,
                )
                ftps.prot_p()
                ftps.set_pasv(True)

                ftps.cwd(self.ftps_upload_path)
                mat_num_dir_name = "no" + self.material_num
                if mat_num_dir_name in ftps.nlst("."):
                    logger.info(
                        {
                            "action": "upload_file",
                            "message": "Directory already exist",
                        }
                    )
                    return False
                ftps.mkd(mat_num_dir_name)
                ftps.cwd(mat_num_dir_name)
                logger.info(
                    {
                        "action": "upload_file",
                        "message": "Upload directory: " + ftps.pwd(),
                    }
                )

                total = len(upload_list)
                for idx, file_path in enumerate(upload_list, start=1):
                    with file_path.open(mode="rb") as file:
                        ftps.storbinary(
                            "STOR " + file_path.name,
                            file,
                        )
                        logger.info(
                            {
                                "action": "upload_file",
                                "message": f"Uploading...: ({idx}/{total}){file_path }",
                            }
                        )

            except all_errors as err:
                logger.error(
                    {
                        "action": "upload_file",
                        "error": f"Upload failed: {err}",
                    }
                )
                return False
            else:
                logger.info(
                    {
                        "action": "upload_file",
                        "message": "Upload completed",
                    }
                )

        return True

    def create_url_text(self) -> None:
        """Create URL text function.

        Write and save the URLs(including short URLs) in the text file.

        Returns:
            None.

        """
        host_zip_file_path = (
            f"{settings.ftps_home_url}{self.ftps_upload_path}no{self.material_num}/"
        )
        local_text_file_path = f"{settings.text_work_dir}url.txt"

        with open(local_text_file_path, "w", encoding="utf-8") as txt:
            for size in self.image_sizes:
                zip_short_url = utils.get_short_url(
                    host_zip_file_path + f"No{self.material_num}-{size}.zip"
                )
                txt.write(zip_short_url + "\n")
            txt.write("\n")

            s_files = self.file_lists_dict[settings.s_size]
            m_files = self.file_lists_dict[settings.m_size]
            l_files = self.file_lists_dict[settings.l_size]
            count = len(s_files)
            for i in range(count):
                txt.write(host_zip_file_path + s_files[i] + "\n")
                txt.write(host_zip_file_path + m_files[i] + "\n")
                txt.write(host_zip_file_path + l_files[i] + "\n\n")

        logger.info(
            {
                "action": "create_url_text",
                "message": "Created url text",
            }
        )
