import base64
import os
from tempfile import NamedTemporaryFile


def get_png_url_from_svg(svg_string, parameters=None):
    if parameters is None:
        parameters = {}

    encoding = parameters.get("encoding", "utf-8")

    svg_file_path = NamedTemporaryFile(suffix=".svg")
    svg_file_path.close()
    svg_file_path = svg_file_path.name

    png_file_path = NamedTemporaryFile(suffix=".png")
    png_file_path.close()
    png_file_path = png_file_path.name

    with open(svg_file_path, "w") as svg_file:
        svg_file.write(svg_string)

    os.system("convert " + svg_file_path + " " + png_file_path)

    base64_bytes = base64.b64encode(open(png_file_path, "rb").read())
    base64_string = base64_bytes.decode(encoding)

    return f"data:image/png;base64,{base64_string} "
