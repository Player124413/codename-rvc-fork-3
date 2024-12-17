import os
import shutil
import sys
from multiprocessing import cpu_count

import gradio as gr

from assets.i18n.i18n import I18nAuto
from core import (
    run_extract_script,
    run_index_script,
    run_preprocess_script,
    run_prerequisites_script,
    run_train_script,
)
from rvc.configs.config import get_gpu_info, get_number_of_gpus, max_vram_gpu
from rvc.lib.utils import format_title
from tabs.settings.sections.restart import stop_train

i18n = I18nAuto()
now_dir = os.getcwd()
sys.path.append(now_dir)

pretraineds_v1 = [
    (
        "pretrained_v1/",
        [
            "D32k.pth",
            "D40k.pth",
            "D48k.pth",
            "G32k.pth",
            "G40k.pth",
            "G48k.pth",
            "f0D32k.pth",
            "f0D40k.pth",
            "f0D48k.pth",
            "f0G32k.pth",
            "f0G40k.pth",
            "f0G48k.pth",
        ],
    ),
]

folder_mapping = {
    "pretrained_v1/": "rvc/models/pretraineds/pretrained_v1/",
}

sup_audioext = {
    "wav",
    "mp3",
    "flac",
    "ogg",
    "opus",
    "m4a",
    "mp4",
    "aac",
    "alac",
    "wma",
    "aiff",
    "webm",
    "ac3",
}

# Custom Pretraineds
pretraineds_custom_path = os.path.join(
    now_dir, "rvc", "models", "pretraineds", "pretraineds_custom"
)

pretraineds_custom_path_relative = os.path.relpath(pretraineds_custom_path, now_dir)

custom_embedder_root = os.path.join(
    now_dir, "rvc", "models", "embedders", "embedders_custom"
)
custom_embedder_root_relative = os.path.relpath(custom_embedder_root, now_dir)

os.makedirs(custom_embedder_root, exist_ok=True)
os.makedirs(pretraineds_custom_path_relative, exist_ok=True)


def get_pretrained_list(suffix):
    return [
        os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk(pretraineds_custom_path_relative)
        for filename in filenames
        if filename.endswith(".pth") and suffix in filename
    ]


pretraineds_list_d = get_pretrained_list("D")
pretraineds_list_g = get_pretrained_list("G")


def refresh_custom_pretraineds():
    return (
        {"choices": sorted(get_pretrained_list("G")), "__type__": "update"},
        {"choices": sorted(get_pretrained_list("D")), "__type__": "update"},
    )


# Dataset Creator
datasets_path = os.path.join(now_dir, "assets", "datasets")

if not os.path.exists(datasets_path):
    os.makedirs(datasets_path)

datasets_path_relative = os.path.relpath(datasets_path, now_dir)


def get_datasets_list():
    return [
        dirpath
        for dirpath, _, filenames in os.walk(datasets_path_relative)
        if any(filename.endswith(tuple(sup_audioext)) for filename in filenames)
    ]


def refresh_datasets():
    return {"choices": sorted(get_datasets_list()), "__type__": "update"}


# Model Names
models_path = os.path.join(now_dir, "logs")


def get_models_list():
    return [
        os.path.basename(dirpath)
        for dirpath in os.listdir(models_path)
        if os.path.isdir(os.path.join(models_path, dirpath))
        and all(excluded not in dirpath for excluded in ["zips", "mute", "reference"])
    ]


def refresh_models():
    return {"choices": sorted(get_models_list()), "__type__": "update"}


# Refresh Models and Datasets
def refresh_models_and_datasets():
    return (
        {"choices": sorted(get_models_list()), "__type__": "update"},
        {"choices": sorted(get_datasets_list()), "__type__": "update"},
    )


# Refresh Custom Embedders
def get_embedder_custom_list():
    return [
        os.path.join(dirpath, dirname)
        for dirpath, dirnames, _ in os.walk(custom_embedder_root_relative)
        for dirname in dirnames
    ]


def refresh_custom_embedder_list():
    return {"choices": sorted(get_embedder_custom_list()), "__type__": "update"}


# Drop Model
def save_drop_model(dropbox):
    if ".pth" not in dropbox:
        gr.Info(
            i18n(
                "The file you dropped is not a valid pretrained file. Please try again."
            )
        )
    else:
        file_name = os.path.basename(dropbox)
        pretrained_path = os.path.join(pretraineds_custom_path_relative, file_name)
        if os.path.exists(pretrained_path):
            os.remove(pretrained_path)
        shutil.copy(dropbox, pretrained_path)
        gr.Info(
            i18n(
                "Click the refresh button to see the pretrained file in the dropdown menu."
            )
        )
    return None


# Drop Dataset
def save_drop_dataset_audio(dropbox, dataset_name):
    if not dataset_name:
        gr.Info("Please enter a valid dataset name. Please try again.")
        return None, None
    else:
        file_extension = os.path.splitext(dropbox)[1][1:].lower()
        if file_extension not in sup_audioext:
            gr.Info("The file you dropped is not a valid audio file. Please try again.")
        else:
            dataset_name = format_title(dataset_name)
            audio_file = format_title(os.path.basename(dropbox))
            dataset_path = os.path.join(now_dir, "assets", "datasets", dataset_name)
            if not os.path.exists(dataset_path):
                os.makedirs(dataset_path)
            destination_path = os.path.join(dataset_path, audio_file)
            if os.path.exists(destination_path):
                os.remove(destination_path)
            shutil.copy(dropbox, destination_path)
            gr.Info(
                i18n(
                    "The audio file has been successfully added to the dataset. Please click the preprocess button."
                )
            )
            dataset_path = os.path.dirname(destination_path)
            relative_dataset_path = os.path.relpath(dataset_path, now_dir)

            return None, relative_dataset_path


# Drop Custom Embedder
def create_folder_and_move_files(folder_name, bin_file, config_file):
    if not folder_name:
        return "Folder name must not be empty."

    folder_name = os.path.join(custom_embedder_root, folder_name)
    os.makedirs(folder_name, exist_ok=True)

    if bin_file:
        bin_file_path = os.path.join(folder_name, os.path.basename(bin_file))
        shutil.copy(bin_file, bin_file_path)

    if config_file:
        config_file_path = os.path.join(folder_name, os.path.basename(config_file))
        shutil.copy(config_file, config_file_path)

    return f"Files moved to folder {folder_name}"


def refresh_embedders_folders():
    custom_embedders = [
        os.path.join(dirpath, dirname)
        for dirpath, dirnames, _ in os.walk(custom_embedder_root_relative)
        for dirname in dirnames
    ]
    return custom_embedders


# Export
## Get Pth and Index Files
def get_pth_list():
    return [
        os.path.relpath(os.path.join(dirpath, filename), now_dir)
        for dirpath, _, filenames in os.walk(models_path)
        for filename in filenames
        if filename.endswith(".pth")
    ]


def get_index_list():
    return [
        os.path.relpath(os.path.join(dirpath, filename), now_dir)
        for dirpath, _, filenames in os.walk(models_path)
        for filename in filenames
        if filename.endswith(".index") and "trained" not in filename
    ]


def refresh_pth_and_index_list():
    return (
        {"choices": sorted(get_pth_list()), "__type__": "update"},
        {"choices": sorted(get_index_list()), "__type__": "update"},
    )


## Export Pth and Index Files
def export_pth(pth_path):
    if pth_path and os.path.exists(pth_path):
        return pth_path
    return None


def export_index(index_path):
    if index_path and os.path.exists(index_path):
        return index_path
    return None


## Upload to Google Drive
def upload_to_google_drive(pth_path, index_path):
    def upload_file(file_path):
        if file_path:
            try:
                gr.Info(f"Uploading {pth_path} to Google Drive...")
                google_drive_folder = "/content/drive/MyDrive/Codename-RVC-Fork-Exported"
                if not os.path.exists(google_drive_folder):
                    os.makedirs(google_drive_folder)
                google_drive_file_path = os.path.join(
                    google_drive_folder, os.path.basename(file_path)
                )
                if os.path.exists(google_drive_file_path):
                    os.remove(google_drive_file_path)
                shutil.copy2(file_path, google_drive_file_path)
                gr.Info("File uploaded successfully.")
            except Exception as error:
                print(f"An error occurred uploading to Google Drive: {error}")
                gr.Info("Error uploading to Google Drive")

    upload_file(pth_path)
    upload_file(index_path)


# Train Tab
def train_tab():
    with gr.Row():
        model_name = gr.Dropdown(
            label=i18n("Model Name"),
            info=i18n("Name of the new model."),
            choices=get_models_list(),
            value="example-model-name",
            interactive=True,
            allow_custom_value=True,
        )
        sampling_rate = gr.Radio(
            label=i18n("Sampling Rate"),
            info="The sampling rate of the model you wanna train. \n( If possible, should match your dataset. Small deviations are allowed. )",
            choices=["32000", "40000", "44100", "48000"],
            value="44100",
            interactive=True,
        )
        vocoder = gr.Radio(
            label=i18n("Vocoder"),
            info="Vocoder for audio synthesis: \n- HiFi-GAN:ㅤDEFAULT \n( Works with all clients incl. mainline RVC ) \n\n- MRF HiFi-GAN:ㅤEXPERIMENTAL \n( Higher fidelity; Compatible only with this fork or Applio). \n\n- RefineGAN:ㅤVERY EXPERIMENTAL \n( For now: Dev only / Casual users shouldn't be using it as of yet. )",
            choices=["HiFi-GAN", "MRF HiFi-GAN", "RefineGAN"],
            value="HiFi-GAN",
            interactive=True,
        )
        rvc_version = gr.Radio(
            label=i18n("Model Architecture"),
            info=i18n("Version of the model architecture."),
            choices=["v1", "v2"],
            value="v2",
            interactive=True,
            visible=False,
        )
    with gr.Accordion(i18n("Preprocess")):
        dataset_path = gr.Dropdown(
            label=i18n("Dataset Path"),
            info="Path to the dataset folder. ( Or you can use the dropbox to browse the folders. )",
            # placeholder=i18n("Enter dataset path"),
            choices=get_datasets_list(),
            allow_custom_value=True,
            interactive=True,
        )
        dataset_creator = gr.Checkbox(
            label=i18n("Dataset Creator"),
            value=False,
            interactive=True,
            visible=True,
        )
        with gr.Column(visible=False) as dataset_creator_settings:
            with gr.Accordion(i18n("Dataset Creator")):
                dataset_name = gr.Textbox(
                    label=i18n("Dataset Name"),
                    info=i18n("Name of the new dataset."),
                    placeholder=i18n("Enter dataset name"),
                    interactive=True,
                )
                upload_audio_dataset = gr.File(
                    label=i18n("Upload Audio Dataset"),
                    type="filepath",
                    interactive=True,
                )
        refresh = gr.Button(i18n("Refresh"))

        with gr.Accordion("Advanced Settings for the preprocessing step", open=False):
            cpu_cores_preprocess = gr.Slider(
                1,
                min(cpu_count(), 32),  # max 32 parallel processes
                min(cpu_count(), 32),
                step=1,
                label=i18n("CPU Cores"),
                info=i18n(
                    "The number of CPU cores to use in the preprocess. The default setting are your cpu cores, which is recommended for most cases."
                ),
                interactive=True,
            )
            with gr.Row():
                cut_preprocess = gr.Checkbox(
                    label=i18n("Audio cutting"),
                    info=i18n(
                        "It's recommended to deactivate this option if your dataset has already been processed."
                    ),
                    value=True,
                    interactive=True,
                    visible=True,
                )
                process_effects = gr.Checkbox(
                    label=i18n("Process effects"),
                    info=i18n(
                        "It's recommended to deactivate this option if your dataset has already been processed."
                    ),
                    value=True,
                    interactive=True,
                    visible=True,
                )
            with gr.Row():
                noise_reduction = gr.Checkbox(
                    label=i18n("Noise Reduction"),
                    info="It's recommended to deactivate this option if your dataset has already been processed.",
                    value=False,
                    interactive=True,
                    visible=True,
                )
                clean_strength = gr.Slider(
                    minimum=0,
                    maximum=1,
                    label=i18n("Noise Reduction Strength"),
                    info=i18n(
                        "Set the clean-up level to the audio you want, the more you increase it the more it will clean up, but it is possible that the audio will be more compressed."
                    ),
                    visible=False,
                    value=0.5,
                    interactive=True,
                )
        preprocess_output_info = gr.Textbox(
            label=i18n("Output Information"),
            info=i18n("The output information will be displayed here."),
            value="",
            max_lines=8,
            interactive=False,
        )

        with gr.Row():
            preprocess_button = gr.Button(i18n("Preprocess Dataset"))
            preprocess_button.click(
                fn=run_preprocess_script,
                inputs=[
                    model_name,
                    dataset_path,
                    sampling_rate,
                    cpu_cores_preprocess,
                    cut_preprocess,
                    process_effects,
                    noise_reduction,
                    clean_strength,
                ],
                outputs=[preprocess_output_info],
            )

    with gr.Accordion(i18n("Extract")):
        with gr.Row():
            f0_method = gr.Radio(
                label=i18n("Pitch extraction algorithm"),
                info="Pitch extraction algorithm to use for the audio conversion: \n\nRMVPE - The default algorithm, which is recommended for most cases; \n- The fastest, very robust to noise. Can tolerate slight harmonies to some degree.  \n\nCREPE - Better suited for truly clean audio where accuracy plays the biggest role; \n- Is slower and way worse in handling noise. Can provide more accurate / softer-ish results. \n\nCEPE-TINY - Smaller / lighter variant of CREPE. \n- Performs worse but is way lighter on hardware. \n\n[ CREPE models have adjustable hop length. ]",
                choices=["crepe", "crepe-tiny", "rmvpe"],
                value="rmvpe",
                interactive=True,
            )

            embedder_model = gr.Radio(
                label=i18n("Embedder Model"),
                info=i18n("Model used for learning speaker embedding."),
                choices=[
                    "contentvec",
                    "chinese-hubert-base",
                    "japanese-hubert-base",
                    "korean-hubert-base",
                    "custom",
                ],
                value="contentvec",
                interactive=True,
            )

        hop_length = gr.Slider(
            1,
            512,
            128,
            step=1,
            label=i18n("Hop Length"),
            info="Adjustable hop lets you choose the granularity / 'resolution' of pitch extraction. \nSmaller the value, longer the extraction/processing takes. ( Higher the hardware usage. ) \n\nCodename;0 recommends: \n- 32: if the voice is heavy on vibratos \n- 64: For general usage \n- 128/256: For when you want decent/okay accuracy but slightly more robust extraction. ( If your audio isn't perfectly clean yet you still wanna use crepe. )",
            visible=False,
            interactive=True,
        )
        with gr.Row(visible=False) as embedder_custom:
            with gr.Accordion("Custom Embedder", open=True):
                with gr.Row():
                    embedder_model_custom = gr.Dropdown(
                        label="Select Custom Embedder",
                        choices=refresh_embedders_folders(),
                        interactive=True,
                        allow_custom_value=True,
                    )
                    refresh_embedders_button = gr.Button("Refresh embedders")
                folder_name_input = gr.Textbox(label="Folder Name", interactive=True)
                with gr.Row():
                    bin_file_upload = gr.File(
                        label="Upload .bin", type="filepath", interactive=True
                    )
                    config_file_upload = gr.File(
                        label="Upload .json", type="filepath", interactive=True
                    )
                move_files_button = gr.Button("Move files to custom embedder folder")

        with gr.Accordion(
            "Override for pitch / features extraction ( For instance, if you wanna use CPU instead of GPU or perhaps, you wanna use multiple GPUs etc. ) By default: GPU's prioritized / preferred. ",
            open=False,
        ):
            with gr.Row():
                with gr.Column():
                    cpu_cores_extract = gr.Slider(
                        1,
                        min(cpu_count(), 32),  # max 32 parallel processes
                        min(cpu_count(), 32),
                        step=1,
                        label=i18n("CPU Cores"),
                        info=i18n(
                            "The number of CPU cores to use in the extraction process. The default setting are your cpu cores, which is recommended for most cases."
                        ),
                        interactive=True,
                    )

                with gr.Column():
                    gpu_extract = gr.Textbox(
                        label=i18n("GPU Number"),
                        info=i18n(
                            "Specify the number of GPUs you wish to utilize for extracting by entering them separated by hyphens (-)."
                        ),
                        placeholder=i18n("0 to ∞ separated by -"),
                        value=str(get_number_of_gpus()),
                        interactive=True,
                    )
                    gr.Textbox(
                        label=i18n("GPU Information"),
                        info=i18n("The GPU information will be displayed here."),
                        value=get_gpu_info(),
                        interactive=False,
                    )

        extract_output_info = gr.Textbox(
            label=i18n("Output Information"),
            info=i18n("The output information will be displayed here."),
            value="",
            max_lines=8,
            interactive=False,
        )
        extract_button = gr.Button(i18n("Extract Features"))
        extract_button.click(
            fn=run_extract_script,
            inputs=[
                model_name,
                rvc_version,
                f0_method,
                hop_length,
                cpu_cores_extract,
                gpu_extract,
                sampling_rate,
                embedder_model,
                embedder_model_custom,
            ],
            outputs=[extract_output_info],
        )

    with gr.Accordion(i18n("Training")):
        with gr.Row():
            batch_size = gr.Slider(
                1,
                50,
                max_vram_gpu(0),
                step=1,
                label=i18n("Batch Size"),
                info="[ TOO BIG BATCH SIZE CAN LEAD TO VRAM 'OOM' ISSUES. ] \nBigger batch size: \n- Promotes smoother, more stable gradients. \n- Can beneficial in cases where your dataset is big and diverse. \n- Can lead to early overtraining or flat / ' stuck ' graphs. \n- Generalization might be worsened. \n\n Smaller batch size: \n- Promotes noisier, less stable gradients. \n- More suitable when your dataset is small, less diverse or repetitive. \n- Can lead to instability / divergence or noisy as hell graphs. \n- Generalization might be improved.",
                interactive=True,
            )
            save_every_epoch = gr.Slider(
                1,
                100,
                10,
                step=1,
                label="Saving frequency",
                info="Determines the saving frequency of epochs. \n For example: Saving every 5th epoch.",
                interactive=True,
            )
            total_epoch = gr.Slider(
                1,
                10000,
                100,
                step=1,
                label="Total Epochs",
                info=i18n(
                    "Specifies the overall quantity of epochs for the model training process."
                ),
                interactive=True,
            )
        with gr.Accordion(i18n("Advanced Settings"), open=False):
            with gr.Row():
                with gr.Column():
                    save_only_latest = gr.Checkbox(
                        label=i18n("Save Only Latest"),
                        info="Enabling this setting will result in the G and D files saving only their most recent versions, \neffectively conserving storage space. \nIn a short: At each save-point, they're getting overwritten. \n\n( Keep it enabled unless you know what you're doing. )",
                        value=True,
                        interactive=True,
                    )
                    save_every_weights = gr.Checkbox(
                        label=i18n("Save Every Weights"),
                        info="This setting saves the model save at each save-point. \n\n( Determined by the ' Save Every Epoch ' slider / counter. )",
                        value=True,
                        interactive=True,
                    )
                    pretrained = gr.Checkbox(
                        label=i18n("Pretrained"),
                        info="Utilize pretrained models ( Generator and Discriminator ) when training your own. \nThis is the only valid approach unless: \n- You're a developer. \n- You 're making a ' from scratch ' model. \n\n( Using pretrains for model creation is referred 'Finetuning' ). ",
                        value=True,
                        interactive=True,
                    )
                with gr.Column():
                    cleanup = gr.Checkbox(
                        label=i18n("Fresh Training"),
                        info="Enable this setting only if you are training a new model from scratch or restarting the training. \nWhat it does is essentially deleting all previously generated weights and tensorboard logs. \n\n( For a model you've specified in 'Model name' )",
                        value=False,
                        interactive=True,
                    )
                    cache_dataset_in_gpu = gr.Checkbox(
                        label=i18n("Cache Dataset in GPU"),
                        info=i18n(
                            "Cache the dataset in GPU memory to speed up the training process. \n NOTE: It is advised to have it turned off \n( Especially if the dataset is large / If you're low on VRAM. ) "
                        ),
                        value=False,
                        interactive=True,
                    )
                    pitch_guidance = gr.Checkbox(
                        label=i18n("Pitch Guidance"),
                        info="Pitch guidance allows for mirroring the intonation and pitch of the original voice. \nThis feature is especially useful for cases where: \n- Maintaining the melody or pitch pattern is crucial. \n - The model's primary purpose is to sing.",
                        value=True,
                        interactive=True,
                    )
            with gr.Column():
                custom_pretrained = gr.Checkbox(
                    label=i18n("Custom Pretrained"),
                    info=i18n(
                        "Utilizing custom pretrained models can lead to superior results, as selecting the most suitable pretrained models tailored to the specific use case can significantly enhance performance."
                    ),
                    value=False,
                    interactive=True,
                )
                with gr.Column(visible=False) as pretrained_custom_settings:
                    with gr.Accordion(i18n("Pretrained Custom Settings")):
                        upload_pretrained = gr.File(
                            label=i18n("Upload Pretrained Model"),
                            type="filepath",
                            interactive=True,
                        )
                        refresh_custom_pretaineds_button = gr.Button(
                            i18n("Refresh Custom Pretraineds")
                        )
                        g_pretrained_path = gr.Dropdown(
                            label=i18n("Custom Pretrained G"),
                            info=i18n(
                                "Select the custom pretrained model for the generator."
                            ),
                            choices=sorted(pretraineds_list_g),
                            interactive=True,
                            allow_custom_value=True,
                        )
                        d_pretrained_path = gr.Dropdown(
                            label=i18n("Custom Pretrained D"),
                            info=i18n(
                                "Select the custom pretrained model for the discriminator."
                            ),
                            choices=sorted(pretraineds_list_d),
                            interactive=True,
                            allow_custom_value=True,
                        )
                multiple_gpu = gr.Checkbox(
                    label=i18n("GPU Settings"),
                    info=(
                        "Lets you set / configure which GPUs you wanna utilize for training the model. ( In case you wanna use more than 1 GPU, that is. )"
                    ),
                    value=False,
                    interactive=True,
                )
                with gr.Column(visible=False) as gpu_custom_settings:
                    with gr.Accordion("GPU ID override / Multi-gpu-training configuration"):
                        gpu = gr.Textbox(
                            label=i18n("GPU Number"),
                            info="Specify the number of GPUs you wish to utilize for training by entering their ID and have them separated by hyphens. (These symbols: -)",
                            placeholder=i18n("0 to ∞ separated by -"),
                            value=str(get_number_of_gpus()),
                            interactive=True,
                        )
                        gr.Textbox(
                            label=i18n("GPU Information"),
                            info=i18n("The GPU information will be displayed here."),
                            value=get_gpu_info(),
                            interactive=False,
                        )
                use_warmup = gr.Checkbox(
                    label="Warmup phase for training",
                    info="Enables usage of warmup for training. ( Currently supports only ' linear lr warmup ' )",
                    value=False,
                    interactive=True,
                )
                with gr.Column(visible=False) as warmup_settings:
                    with gr.Accordion("Warmup settings"):
                        warmup_duration = gr.Slider(
                            1,
                            100,
                            5,
                            step=1,
                            label="Duration of the warmup phase",
                            info="Set the maximum number of epochs you want the warmup phase to last for. For small datasets you can try anywhere from 2 to 10. Alternatively, follow the ' 5–10% of the total epochs ' rule ",
                            interactive=True,
                        )
                use_avg_running_loss = gr.Checkbox(
                    label="Average running loss for training",
                    info="Enables usage of avg running loss for Generator and Discriminator",
                    value=False,
                    interactive=True,
                )
                with gr.Column(visible=False) as avg_running_loss_settings:
                    with gr.Accordion("Avg running loss settings"):
                        n_value_custom = gr.Slider(
                            1,
                            100000,
                            0,
                            step=1,
                            label="Frequency of avg running loss",
                            info="Set the frequency of averaging of the running loss. ( It follows the ' Average every N steps or N mini-batches ' rule )",
                            interactive=True,
                        )
                index_algorithm = gr.Radio(
                    label=i18n("Index Algorithm"),
                    info=i18n(
                        "KMeans is a clustering algorithm that divides the dataset into K clusters. This setting is particularly useful for large datasets."
                    ),
                    choices=["Auto", "Faiss", "KMeans"],
                    value="Auto",
                    interactive=True,
                )

        def enforce_terms(terms_accepted, *args):
                if not terms_accepted:
                    message = "You must agree to the Terms of Use to proceed."
                    gr.Info(message)
                    return message
                return run_train_script(*args)


        terms_checkbox = gr.Checkbox(
            label=i18n("I agree to the terms of use"),
            info=i18n(
                "Please ensure compliance with the terms and conditions detailed in [this document](https://github.com/codename0og/codename-rvc-fork-3/blob/main/TERMS_OF_USE.md) before proceeding with your training."
            ),
            value=False,
            interactive=True,
        )
        train_output_info = gr.Textbox(
                label=i18n("Output Information"),
                info=i18n("The output information will be displayed here."),
                value="",
                max_lines=8,
                interactive=False,
            )

        with gr.Row():
            train_button = gr.Button(i18n("Start Training"))
            train_button.click(
                fn=enforce_terms,
                inputs=[
                    terms_checkbox,
                    model_name,
                    rvc_version,
                    save_every_epoch,
                    save_only_latest,
                    save_every_weights,
                    total_epoch,
                    sampling_rate,
                    batch_size,
                    gpu,
                    pitch_guidance,
                    use_warmup,
                    warmup_duration,
                    n_value_custom,
                    pretrained,
                    cleanup,
                    index_algorithm,
                    cache_dataset_in_gpu,
                    custom_pretrained,
                    g_pretrained_path,
                    d_pretrained_path,
                    vocoder,
                ],
                outputs=[train_output_info],
            )

            stop_train_button = gr.Button(i18n("Stop Training"), visible=False)
            stop_train_button.click(
                fn=stop_train,
                inputs=[model_name],
                outputs=[],
            )

            index_button = gr.Button(i18n("Generate Index"))
            index_button.click(
                fn=run_index_script,
                inputs=[model_name, rvc_version, index_algorithm],
                outputs=[train_output_info],
            )

    with gr.Accordion(i18n("Export Model"), open=False):
        if not os.name == "nt":
            gr.Markdown(
                i18n(
                    "The button 'Upload' is only for google colab: Uploads the exported files to the ApplioExported folder in your Google Drive."
                )
            )
        with gr.Row():
            with gr.Column():
                pth_file_export = gr.File(
                    label=i18n("Exported Pth file"),
                    type="filepath",
                    value=None,
                    interactive=False,
                )
                pth_dropdown_export = gr.Dropdown(
                    label=i18n("Pth file"),
                    info=i18n("Select the pth file to be exported"),
                    choices=get_pth_list(),
                    value=None,
                    interactive=True,
                    allow_custom_value=True,
                )
            with gr.Column():
                index_file_export = gr.File(
                    label=i18n("Exported Index File"),
                    type="filepath",
                    value=None,
                    interactive=False,
                )
                index_dropdown_export = gr.Dropdown(
                    label=i18n("Index File"),
                    info=i18n("Select the index file to be exported"),
                    choices=get_index_list(),
                    value=None,
                    interactive=True,
                    allow_custom_value=True,
                )
        with gr.Row():
            with gr.Column():
                refresh_export = gr.Button(i18n("Refresh"))
                if not os.name == "nt":
                    upload_exported = gr.Button(i18n("Upload"), variant="primary")
                    upload_exported.click(
                        fn=upload_to_google_drive,
                        inputs=[pth_dropdown_export, index_dropdown_export],
                        outputs=[],
                    )

            def toggle_visible(checkbox):
                return {"visible": checkbox, "__type__": "update"}

            def toggle_visible_hop_length(f0_method):
                if f0_method == "crepe" or f0_method == "crepe-tiny":
                    return {"visible": True, "__type__": "update"}
                return {"visible": False, "__type__": "update"}

            def toggle_pretrained(pretrained, custom_pretrained):
                if custom_pretrained == False:
                    return {"visible": pretrained, "__type__": "update"}, {
                        "visible": False,
                        "__type__": "update",
                    }
                else:
                    return {"visible": pretrained, "__type__": "update"}, {
                        "visible": pretrained,
                        "__type__": "update",
                    }

            def enable_stop_train_button():
                return {"visible": False, "__type__": "update"}, {
                    "visible": True,
                    "__type__": "update",
                }

            def disable_stop_train_button():
                return {"visible": True, "__type__": "update"}, {
                    "visible": False,
                    "__type__": "update",
                }

            def download_prerequisites(version, pitch_guidance):
                if version == "v1":
                    if pitch_guidance:
                        gr.Info(
                            "Checking for v1 prerequisites with pitch guidance... Missing files will be downloaded. If you already have them, this step will be skipped."
                        )
                        run_prerequisites_script(
                            pretraineds_v1_f0=True,
                            pretraineds_v1_nof0=False,
                            pretraineds_v2_f0=False,
                            pretraineds_v2_nof0=False,
                            models=False,
                            exe=False,
                        )
                    else:
                        gr.Info(
                            "Checking for v1 prerequisites without pitch guidance... Missing files will be downloaded. If you already have them, this step will be skipped."
                        )
                        run_prerequisites_script(
                            pretraineds_v1_f0=False,
                            pretraineds_v1_nof0=True,
                            pretraineds_v2_f0=False,
                            pretraineds_v2_nof0=False,
                            models=False,
                            exe=False,
                        )
                elif version == "v2":
                    if pitch_guidance:
                        gr.Info(
                            "Checking for v2 prerequisites with pitch guidance... Missing files will be downloaded. If you already have them, this step will be skipped."
                        )
                        run_prerequisites_script(
                            pretraineds_v1_f0=False,
                            pretraineds_v1_nof0=False,
                            pretraineds_v2_f0=True,
                            pretraineds_v2_nof0=False,
                            models=False,
                            exe=False,
                        )
                    else:
                        gr.Info(
                            "Checking for v2 prerequisites without pitch guidance... Missing files will be downloaded. If you already have them, this step will be skipped."
                        )
                        run_prerequisites_script(
                            pretraineds_v1_f0=False,
                            pretraineds_v1_nof0=False,
                            pretraineds_v2_f0=False,
                            pretraineds_v2_nof0=True,
                            models=False,
                            exe=False,
                        )
                gr.Info(
                    "Prerequisites check complete. Missing files were downloaded, and you may now start preprocessing."
                )

            def toggle_visible_embedder_custom(embedder_model):
                if embedder_model == "custom":
                    return {"visible": True, "__type__": "update"}
                return {"visible": False, "__type__": "update"}

            def update_slider_visibility(noise_reduction):
                return gr.update(visible=noise_reduction)

            noise_reduction.change(
                fn=update_slider_visibility,
                inputs=noise_reduction,
                outputs=clean_strength,
            )
            rvc_version.change(
                fn=download_prerequisites,
                inputs=[rvc_version, pitch_guidance],
                outputs=[],
            )

            pitch_guidance.change(
                fn=download_prerequisites,
                inputs=[rvc_version, pitch_guidance],
                outputs=[],
            )

            refresh.click(
                fn=refresh_models_and_datasets,
                inputs=[],
                outputs=[model_name, dataset_path],
            )

            dataset_creator.change(
                fn=toggle_visible,
                inputs=[dataset_creator],
                outputs=[dataset_creator_settings],
            )

            upload_audio_dataset.upload(
                fn=save_drop_dataset_audio,
                inputs=[upload_audio_dataset, dataset_name],
                outputs=[upload_audio_dataset, dataset_path],
            )

            f0_method.change(
                fn=toggle_visible_hop_length,
                inputs=[f0_method],
                outputs=[hop_length],
            )

            embedder_model.change(
                fn=toggle_visible_embedder_custom,
                inputs=[embedder_model],
                outputs=[embedder_custom],
            )
            embedder_model.change(
                fn=toggle_visible_embedder_custom,
                inputs=[embedder_model],
                outputs=[embedder_custom],
            )
            move_files_button.click(
                fn=create_folder_and_move_files,
                inputs=[folder_name_input, bin_file_upload, config_file_upload],
                outputs=[],
            )
            refresh_embedders_button.click(
                fn=refresh_embedders_folders, inputs=[], outputs=[embedder_model_custom]
            )
            pretrained.change(
                fn=toggle_pretrained,
                inputs=[pretrained, custom_pretrained],
                outputs=[custom_pretrained, pretrained_custom_settings],
            )

            custom_pretrained.change(
                fn=toggle_visible,
                inputs=[custom_pretrained],
                outputs=[pretrained_custom_settings],
            )

            refresh_custom_pretaineds_button.click(
                fn=refresh_custom_pretraineds,
                inputs=[],
                outputs=[g_pretrained_path, d_pretrained_path],
            )

            upload_pretrained.upload(
                fn=save_drop_model,
                inputs=[upload_pretrained],
                outputs=[upload_pretrained],
            )

            use_warmup.change(
                fn=toggle_visible,
                inputs=[use_warmup],
                outputs=[warmup_settings],
            )

            use_avg_running_loss.change(
                fn=toggle_visible,
                inputs=[use_avg_running_loss],
                outputs=[avg_running_loss_settings],
            )

            multiple_gpu.change(
                fn=toggle_visible,
                inputs=[multiple_gpu],
                outputs=[gpu_custom_settings],
            )

            train_button.click(
                fn=enable_stop_train_button,
                inputs=[],
                outputs=[train_button, stop_train_button],
            )

            train_output_info.change(
                fn=disable_stop_train_button,
                inputs=[],
                outputs=[train_button, stop_train_button],
            )

            pth_dropdown_export.change(
                fn=export_pth,
                inputs=[pth_dropdown_export],
                outputs=[pth_file_export],
            )

            index_dropdown_export.change(
                fn=export_index,
                inputs=[index_dropdown_export],
                outputs=[index_file_export],
            )

            refresh_export.click(
                fn=refresh_pth_and_index_list,
                inputs=[],
                outputs=[pth_dropdown_export, index_dropdown_export],
            )
