# To run this script, use the following command:
# python main.py data.pdf --output-format json --output-dir output
# python main.py data.pdf --output-format markdown --output-dir output


from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.renderers.json import JSONOutput
from marker.renderers.markdown import MarkdownOutput
from typing import Optional
import json, argparse, os


parser = argparse.ArgumentParser(description="Convert a PDF file to a JSON file.")
parser.add_argument("input_file", type=str, help="The PDF file to convert.")
parser.add_argument("--output-format", type=str, default="json", help="The output format to use.")
parser.add_argument("--output-dir", type=str, default="output", help="The output directory to save the file.")
args = parser.parse_args()


def save_data(
        data: Optional[JSONOutput | MarkdownOutput],
        output_path: str
    ) -> bool:
    """
    Saves the data to a JSON file or markdown file.
    """

    if output_path.endswith(".json"):
        try:
            struc_data = data.model_dump()
            struc_data.pop("metadata", None)
            struc_data.pop("block_type", None)
            with open(output_path, "w") as f:
                remove_extra(struc_data)
                json.dump(struc_data, f, indent=4)
                print(f"\nOutput saved to {output_path}")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    else:
        # Save as markdown
        try:
            with open(output_path, "w") as f:
                f.write(data.markdown)
                print(f"\nOutput saved to {output_path}")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


def remove_extra(
        obj: dict | list
    ) -> None:
    if isinstance(obj, dict):
        obj.pop('polygon', None)
        obj.pop('bbox', None)
        # Recursively call on each value
        for key, value in obj.items():
            remove_extra(value)
    elif isinstance(obj, list):
        for item in obj:
            remove_extra(item)


def parse_pdf(
        input_file: str,
        output_format: str,
        output_dir: str
    ) -> Optional[JSONOutput | MarkdownOutput]:
    """
    Parses a PDF file and saves the output in the specified format and directory.
    """
    config = {
        "output_format": output_format,
        "output_dir": output_dir,
        "ADDITIONAL_KEY": "VALUE",

        "use_llm": True,
        "llm_service": 'marker.services.ollama.OllamaService',
        "ollama_base_url": "http://127.0.0.1:11434/",
        "ollama_model": "llama3.1:8b",

        "page_range": "1",
    }
    config_parser = ConfigParser(config)

    converter = PdfConverter(
        config=config_parser.generate_config_dict(), # User defined config
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service()
    )
    parsed_data = converter(input_file)

    return parsed_data


if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")    
    output_format : str = args.output_format
    output_dir : str = args.output_dir
    input_file : str = args.input_file

    print(f"\nConverting {input_file} to {output_format} format...")
    print(f"Output will be saved to {output_dir}\n")

    output : Optional[JSONOutput | MarkdownOutput] = parse_pdf(input_file, output_format, output_dir)

    output_file : str = f"{output_dir}/output.json" \
                        if output_format == "json" \
                        else f"{output_dir}/output.md"
    is_saved : bool = save_data(output, output_file)

    if is_saved:
        print("\nConversion successful ✔")
    else:
        print("\nConversion failed ❌")
