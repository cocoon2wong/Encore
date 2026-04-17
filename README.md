<!--
 * @Author: Conghao Wong
 * @Date: 2026-01-29 19:26:52
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2026-04-17 14:53:41
 * @Github: https://cocoon2wong.github.io
 * Copyright 2026 Conghao Wong, All Rights Reserved.
-->

# Encore

This is the official code repo of our paper "Encore: Conditioning Trajectory Forecasting via Biased Ego Rehearsals".
The full paper will be made available on arXiv soon.
Our model weights are available at [this page](https://github.com/cocoon2wong/Project-Monandaeg/tree/Enc).

## Getting Started

You can clone [this repository](https://github.com/cocoon2wong/Encore) by the following command:

```bash
git clone https://github.com/cocoon2wong/Encore.git
```

Then, run the following command to initialize all submodules (Submodules include our unified training engine (`qpid`) and dataset processing utilities):

```bash
git submodule update --init --recursive
```

## Requirements

The code is developed with Python 3.10.
Additional packages used are included in the `requirements.txt` file.

> [!WARNING]
> We recommend installing all required Python packages in a virtual environment (like the `conda` environment).
> Otherwise, there *COULD* be other problems due to the package version conflicts.

Run the following command to install the required packages in your Python environment:

```bash
pip install -r requirements.txt
```

## Preparing Datasets

### ETH-UCY, SDD, nuScenes, NBA

> [!WARNING]
> If you want to validate `Encore` models on these datasets, make sure you are getting this repository via `git clone` and that all *git submodules* have been properly initialized via `git submodule update --init --recursive`.

You can run the following commands to prepare dataset files that have been validated in our paper:

1. Run Python the script inner the `dataset_original` folder:

    ```bash
    cd dataset_original
    ```

    - For `ETH-UCY` and `SDD`, run

        ```bash
        python main_ethucysdd.py
        ```

        > [!NOTE]
        > Our reported results and provided weights on the `eth` set is actually the 6-frame-interval version.
        > To test the 10-frame-sampled eth, please run `python codes/ethucy/create_10sampled_eth_data.py`, then use the clip name `eth10` to train or test models.
        > For more information and notes our used datasets and splits, please refer to [this page](https://projectunpredictable.com/Project-Qpid/docs/dataset/dataset-and-split-notes/).

    - For `nuScenes`, please download their dataset files, put them into the given path listed within `dataset_original/main_nuscenes.py`, then run

        ```bash
        python main_nuscenes.py
        ```

    - For `NBA`, please download their dataset files, put them into the given path listed within `dataset_original/main_nba.py`, then run

        ```bash
        python main_nba.py
        ```

        Please note that the training/test/validate splits will be selected randomly, provided that the total dataset size is approximately 50,000 ego agents.
        This may result in different metrics for our pre-trained models.
        If you wish to fully reproduce our results, please download our processed dataset files from [this page](https://github.com/cocoon2wong/Project-Luna/releases).

2. Back to the repo folder and create soft links:

    ```bash
    cd ..
    ln -s dataset_original/dataset_processed ./
    ln -s dataset_original/dataset_configs ./
    ```

> [!NOTE]
> You can also download our processed dataset files manually from [this page](https://github.com/cocoon2wong/Project-Luna/releases), and put them into `dataset_processed` and `dataset_configs` folders manually to reproduce our results.

Click the following buttons to learn how we process these dataset files and the detailed dataset settings.

<div class="btn-normal-group" style="text-align: center;">
    <a class="btn btn-lg btn-normal" href="https://cocoon2wong.github.io/Project-Luna/howToUse/">💡 Dataset Guidelines</a>
    <a class="btn btn-lg btn-normal" href="https://cocoon2wong.github.io/Project-Luna/notes/">💡 Datasets and Splits Information</a>
</div>

### Training on Your New Datasets

Before training `Encore` models on your own datasets, you should add your dataset information in the above `dataset_processed`/`dataset_configs` way.
See [this page](https://cocoon2wong.github.io/Project-Luna/) for more details.

## Model Weights

We have provided our pre-trained model weights to help you quickly evaluate `Encore` models' performance.

Click the following buttons to download our model weights.
We recommend that you download the weights and place them in the `weights` folder.

<div class="btn-normal-group" style="text-align: center;">
    <a class="btn btn-lg btn-normal" href="https://github.com/cocoon2wong/Project-Monandaeg/tree/Enc">📂 Weights Repo</a>
    <a class="btn btn-lg btn-normal" href="https://github.com/cocoon2wong/Project-Monandaeg/archive/refs/heads/Enc.zip">⬇️ Download Weights</a>
</div>

You can start evaluating these weights by

```bash
python main.py --load SOME_MODEL_WEIGHTS
```

Here, `SOME_MODEL_WEIGHTS` is the path of the weights folder, for example, `./weights/enczara1`.

## Training

You can start training an `Encore` model via the following command:

```bash
python main.py --model enc --split DATASET_SPLIT
```

Here, `DATASET_SPLIT` is the identifier (i.e., the name of dataset's split files in `dataset_configs`, for example `eth` is the identifier of the split list in `dataset_configs/ETH-UCY/eth.plist`) of the dataset or splits used for training.
It accepts:

- ETH-UCY: {`eth`, `hotel`, `univ13`, `zara1`, `zara2`};
- SDD: `sdd`;
- nuScenes: `nuScenes_ov_v1.0`;
- NBA: `nba50k`.

For example, you can start training the `Encore` model on the `zara1` split by

```bash
python main.py --model enc --split zara1 --batch_size 1500 --epochs 300
```

Also, other args may need to be specified, like the learning rate `--lr`, batch size `--batch_size`, etc.
See detailed args in the [Args Used](#args-used) Section.

## Reproducing Our Results

The simplest way to reproduce our results is to copy all training args we used in the provided weights.
For example, you can start a training of `Encore` on `zara1` using the same args as we did by:

```bash
python main.py --model enc --restore_args ${PATH_TO_YOUR_DOWNLOADED_WEIGHTS}/enczara1
```

Here, `${PATH_TO_YOUR_DOWNLOADED_WEIGHTS}` is your path to save our pretrained weights, which usually could be named as `Project-Monandaeg-Enc` after downloading.
The `--restore_args` arg only reads settings within the `args.json` file, and it does not load model weights before training.

You can open a `Tensorboard` to see how losses and metrics change during training, by:

```bash
tensorboard --logdir ./logs
```

\\

## Visualization & Playground

We have build a simple user interface to validate the qualitative trajectory prediction performance of our proposed `Encore` models.
You can use it to visualize model predictions and learn how the proposed `Encore` works in an interactive way by adding any manual neighbors at any positions in the scene.

> [!WARNING]
> Visualizations may need dataset videos.
> For copyright reasons and size limitations, we do not provide them in our repo.
> Instead, a static image will be displayed if you have no videos put into the corresponding path.

> [!NOTE]
> If you have these dataset videos, you can name them using the given filename and path specified in the `video_path` within videos' config files (`/dataset_configs/***/subsets/***.plist`, for example `/dataset_configs/ETH-UCY/subsets/zara1.plist`) to load and visualize them properly.

This playground interface is implemented with `PyQt6`.
Install this package in your python environment to start:

```bash
pip install pyqt6
```

Run the following command to open a playground:

```bash
python playground/main.py
```

![Playground](https://raw.githubusercontent.com/cocoon2wong/Encore/main/docs/subassets/img/playground.png)

### Load Models and Datasets

You can load a supported `Encore` model or one of its variations by clicking the `Load Model` button.
By clicking the `Run` button, you can see how the loaded model performs on the given sample.
You can also load different datasets (video clips) by clicking the `More Settings ...` button.

### Add Manual Neighbors

You can also directly click the visualized figure to add a new neighbor to the scene.
Through this neighbor that wasn't supposed to exist in the prediction scene, you can verify how models handle *social interactions* qualitatively.

### The `Encore` Playground

To deeply understand how the `Encore` model works internally, we provide several args to visualize the intermediate processes, including the biased rehearsals forecasted by the Ego Predictor, the learned insight kernels, and the feature-level conditioning activations.

> [!WARNING]
> All the following visualization args only work in the **Playground** mode.
> Ensure you are running the `playground/main.py` script.

#### Visualize Biased Ego Rehearsals

You can use the arg `--vis_ego_predictor` to visualize the short-term rehearsal trajectories forecasted by the ego predictor.
For example, you can use the following command to open a playground with a pretrained model (e.g., our `zara1` pretrained weights) and visualize the specific biased rehearsals:

```bash
python playground/main.py --load ./${PATH_TO_THE_WEIGHTS}$/enczara1 --vis_ego_predictor 1
```

The arg `--vis_ego_predictor` accepts four kinds of string values:

- `0`: Do nothing *(Default)*.
- `1`: Visualize **all** multimodal predictions of the ego predictor.
- `2`: Visualize the ego predictor's **mean prediction** for each neighbor.
- `k<n>`: Visualize the specific **$n$-th rehearsal** (from all $K_I$ insights).
    For example, `--vis_ego_predictor k1` visualizes the first rehearsal mode.
    Note that $n$ should be strictly less than the number of insights (which is controlled by the arg `--insights`).

In the playground, click `Random` to select a prediction sample and click `Run` to visualize these rehearsals in the environment.
Also, args `--pred_color_mode 1` and `--draw_lines` are recommend for the better visualization.
The `Encore` arg `--ego_capacity` also limits the number of neighbors to compute these non-linear rehearsals (like we elaborated in the implementation details section).
You can set it to a larger value when visualization, for example `--ego_capacity 20`:

![Playground: Rehearsals Visualization](https://raw.githubusercontent.com/cocoon2wong/Encore/main/docs/subassets/img/playground_ego_predictor.png)

Command used:

```bash
python playground/main.py \
    -l ../Project-Monandaeg-Enc/enczara1 \
    --vis-ego-predictor 1 \
    --pred-color-mode 1 \
    --draw-lines \
    --ego-capacity 20
```

#### Visualize Insight Kernels

You can add the arg `--vis_insight_kernels` to visualize the distribution of time-averaged insight kernels learned by the ego predictor, learning how the distinct ego biases have been learned and distributed:

![Playground: Insight Kernels](https://raw.githubusercontent.com/cocoon2wong/Encore/main/docs/subassets/img/playground_insight_kernels.png)

Command used:

```bash
python playground/main.py \
    -l ../Project-Monandaeg-Enc/enczara1 \
    --vis_insight_kernels \
    --draw_neighbor_IDs \
    --draw_groundtruths 0
```

#### Visualize Feature Activations

You can also visualize how the final predictor selectively activates specific rehearsal features during the bias-conditioning process.

We provide two separate arguments for visualizing self activations and social activations:

- To visualize self activations (requires `--use_intention_predictor` enabled during training), please use `--vis_self_activations 1`.
- To visualize social activations (requires `--use_social_predictor` enabled during training), please use `--vis_social_activations 1`.

Both `--vis_self_activations` and `--vis_social_activations` accept the following modes:

  - `0`: Do nothing *(Default)*.
  - `1`: Regular visualization of the feature selection results.
  - `2`: Visualization while additionally displaying the activation rate of the **mean trajectory** (useful for observing the "mean paradox").
  - `3`: Visualize absolute feature deviation instead of activations.

**Special note for `--vis_social_activations`:**
By default, the visualization targets the 0-th neighbor (the ego itself sorted by Euclidean distance).
You can specify different neighbors by concatenating the mode and the neighbor ID with a `_`.
For example, `--vis_social_activations 1_3` means using mode `1` (Regular visualization) and for the target the `3`rd neighbor (whose ID can be visualized by adding the arg `--draw_neighbor_IDs`).

![Playground: Feature Activations](https://raw.githubusercontent.com/cocoon2wong/Encore/main/docs/subassets/img/playground_feature_activations.png)

Command used:

```bash
python playground/main.py \
    -l ../Project-Monandaeg-Enc/enczara1 \
    --vis_social_activations 1_3 \
    --draw_neighbor_IDs
```

<!-- DO NOT CHANGE THIS LINE -->

---

## Args Used

Please specify your customized args when training or testing your model in the following way:

```bash
python main.py --ARG_KEY1 ARG_VALUE2 --ARG_KEY2 ARG_VALUE2 -SHORT_ARG_KEY3 ARG_VALUE3 ...
```

where `ARG_KEY` is the name of args, and `ARG_VALUE` is the corresponding value.
All args and their usages are listed below.

About the `argtype`:

- Args with argtype=`static` can not be changed once after training.
  When testing the model, the program will not parse these args to overwrite the saved values.
- Args with argtype=`dynamic` can be changed anytime.
  The program will try to first parse inputs from the terminal and then try to load from the saved JSON file.
- Args with argtype=`temporary` will not be saved into JSON files.
  The program will parse these args from the terminal at each time.

### Basic Args


<details markdown="1">
<summary markdown="span"><code>--K</code></summary>

The number of multiple generations when testing. This arg only works for multiple-generation models.

- Type=`int`, argtype=`dynamic`
- The default value is `20`.

</details>

<details markdown="1">
<summary markdown="span"><code>--K_train</code></summary>

The number of multiple generations when training. This arg only works for multiple-generation models.

- Type=`int`, argtype=`static`
- The default value is `10`.

</details>

<details markdown="1">
<summary markdown="span"><code>--anntype</code></summary>

Model's predicted annotation type. Can be `'coordinate'` or `'boundingbox'`.

- Type=`str`, argtype=`static`
- The default value is `coordinate`.

</details>

<details markdown="1">
<summary markdown="span"><code>--auto_clear</code></summary>

Controls whether to clear all other saved weights except for the best one. It performs similarly to running `python scripts/clear.py --logs logs`.

- Type=`int`, argtype=`temporary`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--batch_size</code> (short for <code>-bs</code>)</summary>

Batch size when implementation.

- Type=`int`, argtype=`dynamic`
- The default value is `5000`.

</details>

<details markdown="1">
<summary markdown="span"><code>--compute_loss</code></summary>

Controls whether to compute losses when testing.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--compute_metrics_with_types</code></summary>

Controls whether to compute metrics separately on different kinds of agents.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--compute_statistical_metrics</code></summary>

(bool) Choose whether to compute metrics (ADE/FDE) as `mean $\pm$ std`.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--dataset</code></summary>

Name of the video dataset to train or evaluate. For example, `'ETH-UCY'` or `'SDD'`. NOTE: DO NOT set this argument manually.

- Type=`str`, argtype=`static`
- The default value is `Unavailable`.

</details>

<details markdown="1">
<summary markdown="span"><code>--down_sampling_rate</code></summary>

Selects whether to down-sample from multiple-generated predicted trajectories. This arg only works for multiple-generative models.

- Type=`float`, argtype=`temporary`
- The default value is `1.0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_results</code> (short for <code>-dr</code>)</summary>

Controls whether to draw visualized results on video frames. Accept the name of one video clip. The codes will first try to load the video file according to the path saved in the `plist` file (saved in `dataset_configs` folder), and if it loads successfully it will draw the results on that video, otherwise it will draw results on a blank canvas. Note that `test_mode` will be set to `'one'` and `force_split` will be set to `draw_results` if `draw_results != 'null'`.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_videos</code></summary>

Controls whether to draw visualized results on video frames and save them as images. Accept the name of one video clip. The codes will first try to load the video according to the path saved in the `plist` file, and if successful it will draw the visualization on the video, otherwise it will draw on a blank canvas. Note that `test_mode` will be set to `'one'` and `force_split` will be set to `draw_videos` if `draw_videos != 'null'`.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--epochs</code></summary>

Maximum training epochs.

- Type=`int`, argtype=`static`
- The default value is `500`.

</details>

<details markdown="1">
<summary markdown="span"><code>--experimental</code></summary>

NOTE: It is only used for code tests.

- Type=`bool`, argtype=`temporary`
- The default value is `False`.

</details>

<details markdown="1">
<summary markdown="span"><code>--feature_dim</code></summary>

Feature dimensions that are used in most layers.

- Type=`int`, argtype=`static`
- The default value is `128`.

</details>

<details markdown="1">
<summary markdown="span"><code>--force_anntype</code></summary>

Assign the prediction type. It is now only used for silverballers models that are trained with annotation type `coordinate` but to be tested on datasets with annotation type `boundingbox`.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--force_clip</code></summary>

Force test video clip (ignore the train/test split). It only works when `test_mode` has been set to `one`. .

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--force_dataset</code></summary>

Force test dataset (ignore the train/test split). It only works when `test_mode` has been set to `one`.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--force_split</code></summary>

Force test dataset (ignore the train/test split).  It only works when `test_mode` has been set to `one`.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--gpu</code></summary>

Speed up training or test if you have at least one NVidia GPU.  If you have no GPUs or want to run the code on your CPU,  please set it to `-1`. NOTE: It only supports training or testing on one GPU.

- Type=`str`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--help</code> (short for <code>-h</code>)</summary>

Print help information on the screen.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--input_pred_steps</code></summary>

Indices of future time steps that are used as extra model inputs. It accepts a string that contains several integer numbers separated with `'_'`. For example, `'3_6_9'`. It will take the corresponding ground truth points as the input when  training the model, and take the first output of the former network as this input when testing the model. Set it to `'null'` to disable these extra model inputs.

- Type=`str`, argtype=`static`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--interval</code></summary>

Time interval of each sampled trajectory point.

- Type=`float`, argtype=`static`
- The default value is `0.4`.

</details>

<details markdown="1">
<summary markdown="span"><code>--load</code> (short for <code>-l</code>)</summary>

Folder to load model weights (to test). If it is set to `null`, the training manager will start training new models according to other reveived args. NOTE: Leave this arg to `null` when training new models.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--load_epoch</code></summary>

Load model weights that is saved after specific training epochs. It will try to load the weight file in the `load` dir whose name is end with `_epoch${load_epoch}`. This arg only works when the `auto_clear` arg is disabled (by passing `--auto_clear 0` when training). Set it to `-1` to disable this function.

- Type=`int`, argtype=`temporary`
- The default value is `-1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--load_part</code></summary>

Choose whether to load only a part of the model weights if the `state_dict` of the saved model and the model in the code do not match.

*IMPORTANT NOTE*: This arg is only used for some ablation experiments. It MAY lead to incorrect predictions or metrics.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--log_dir</code></summary>

Folder to save training logs and model weights. Logs will save at `${save_base_dir}/${log_dir}`. DO NOT change this arg manually. (You can still change the saving path by passing the `save_base_dir` arg.).

- Type=`str`, argtype=`static`
- The default value is `Unavailable`.

</details>

<details markdown="1">
<summary markdown="span"><code>--loss_weights</code></summary>

Configure the agent-wise loss weights. It now only supports the dataset-clip-wise re-weight.

- Type=`str`, argtype=`dynamic`
- The default value is `{}`.

</details>

<details markdown="1">
<summary markdown="span"><code>--lr</code> (short for <code>-lr</code>)</summary>

Learning rate.

- Type=`float`, argtype=`static`
- The default value is `0.001`.

</details>

<details markdown="1">
<summary markdown="span"><code>--macos</code></summary>

(Experimental) Choose whether to enable the `MPS (Metal Performance Shaders)` on Apple platforms (instead of running on CPUs).

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--max_agents</code></summary>

Max number of agents to predict per frame. It only works when `model_type == 'frame-based'`.

- Type=`int`, argtype=`dynamic`
- The default value is `50`.

</details>

<details markdown="1">
<summary markdown="span"><code>--model</code></summary>

The model type used to train or test.

- Type=`str`, argtype=`static`
- The default value is `none`.

</details>

<details markdown="1">
<summary markdown="span"><code>--model_name</code></summary>

Customized model name.

- Type=`str`, argtype=`static`
- The default value is `model`.

</details>

<details markdown="1">
<summary markdown="span"><code>--model_type</code></summary>

Model type. It can be `'agent-based'` or `'frame-based'`.

- Type=`str`, argtype=`static`
- The default value is `agent-based`.

</details>

<details markdown="1">
<summary markdown="span"><code>--noise_depth</code></summary>

Depth of the random noise vector.

- Type=`int`, argtype=`static`; also: `--depth`
- The default value is `16`.

</details>

<details markdown="1">
<summary markdown="span"><code>--obs_frames</code> (short for <code>-obs</code>)</summary>

Observation frames for prediction.

- Type=`int`, argtype=`static`
- The default value is `8`.

</details>

<details markdown="1">
<summary markdown="span"><code>--output_pred_steps</code></summary>

Indices of future time steps to be predicted. It accepts a string that contains several integer numbers separated with `'_'`. For example, `'3_6_9'`. Set it to `'all'` to predict points among all future steps.

- Type=`str`, argtype=`static`; also: `--key_points`
- The default value is `all`.

</details>

<details markdown="1">
<summary markdown="span"><code>--pmove</code></summary>

(Pre/post-process Arg) Index of the reference point when moving trajectories.

- Type=`int`, argtype=`static`
- The default value is `-1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--pred_frames</code> (short for <code>-pred</code>)</summary>

Prediction frames.

- Type=`int`, argtype=`static`
- The default value is `12`.

</details>

<details markdown="1">
<summary markdown="span"><code>--preprocess</code></summary>

Controls whether to run any pre-process before the model inference. It accepts a 3-bit-like string value (like `'111'`): - The first bit: `MOVE` trajectories to (0, 0); - The second bit: re-`SCALE` trajectories; - The third bit: `ROTATE` trajectories.

- Type=`str`, argtype=`static`
- The default value is `100`.

</details>

<details markdown="1">
<summary markdown="span"><code>--restore</code></summary>

Path to restore the pre-trained weights before training. It will not restore any weights if `args.restore == 'null'`.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--restore_args</code></summary>

Path to restore the reference args before training. It will not restore any args if `args.restore_args == 'null'`.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--save_base_dir</code></summary>

Base folder to save all running logs.

- Type=`str`, argtype=`static`
- The default value is `./logs`.

</details>

<details markdown="1">
<summary markdown="span"><code>--split</code> (short for <code>-s</code>)</summary>

The dataset split that used to train and evaluate.

- Type=`str`, argtype=`static`
- The default value is `zara1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--start_test_percent</code></summary>

Set when (at which epoch) to start validation during training. The range of this arg should be `0 <= x <= 1`.  Validation may start at epoch `args.epochs * args.start_test_percent`.

- Type=`float`, argtype=`temporary`
- The default value is `0.0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--step</code></summary>

Frame interval for sampling training data.

- Type=`float`, argtype=`dynamic`
- The default value is `1.0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--test_mode</code></summary>

Test settings. It can be `'one'`, `'all'`, or `'mix'`. When setting it to `one`, it will test the model on the `args.force_split` only; When setting it to `all`, it will test on each of the test datasets in `args.split`; When setting it to `mix`, it will test on all test datasets in `args.split` together.

- Type=`str`, argtype=`temporary`
- The default value is `mix`.

</details>

<details markdown="1">
<summary markdown="span"><code>--test_step</code></summary>

Epoch interval to run validation during training.

- Type=`int`, argtype=`temporary`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--update_saved_args</code></summary>

Choose whether to update (overwrite) the saved arg files or not.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--verbose</code> (short for <code>-v</code>)</summary>

Controls whether to print verbose logs and outputs to the terminal.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

### Visualization Args


<details markdown="1">
<summary markdown="span"><code>--distribution_steps</code></summary>

Controls which time step(s) to consider when visualizing the distribution of forecasted trajectories. Accepts one or more integers (starting from 0) separated by `'_'`. For example, `'4_8_11'`. Set to `'all'` to show the distribution of all predictions.

- Type=`str`, argtype=`temporary`
- The default value is `all`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_distribution</code> (short for <code>-dd</code>)</summary>

Controls the bandwidth (smoothing) of the predicted trajectory distributions.

- 0.0: Disable distribution drawing; draw as individual points. - > 0.0: Enable KDE distribution drawing, where this value acts as   the `bw_adjust` parameter to control smoothing (e.g., 0.5).

- Type=`float`, argtype=`temporary`
- The default value is `0.0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_exclude_type</code></summary>

Draw visualized results for all agents except those of user-assigned types. If the assigned types are `"Biker_Cart"` and `draw_results` or  `draw_videos` is not `"null"`, it draws results for all agent types except "Biker" and "Cart". It supports partial matching and is  case-sensitive.

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_extra_outputs</code></summary>

(bool) Controls whether to draw (as text) extra model outputs on the visualized images.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_full_neighbors</code></summary>

(bool) Controls whether to draw the full observed trajectories of all neighbor agents, rather than only the last trajectory point at the current observation moment.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_groundtruths</code></summary>

(bool) Controls whether to draw ground-truth trajectories during visualization.

- Type=`int`, argtype=`temporary`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_index</code></summary>

Indices of test agents to visualize. Numbers are separated by `_`. For example, `'123_456_789'`.

- Type=`str`, argtype=`temporary`
- The default value is `all`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_lines</code></summary>

(bool) Controls whether to draw lines between consecutive 2D trajectory points.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_neighbor_IDs</code></summary>

Controls whether to draw the index of neighbors during visualization. It accepts an integer value. Set it to `0` to disable this function. Set it to `1` to visualize all neighbors' IDs, while  set it to an integer larger that `1` will only display this limited number of neighbor IDs.

- Type=`int`, argtype=`temporary`; also: `--draw_neighbor_ids`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_on_empty_canvas</code></summary>

Controls whether to draw on an empty (or a single-colored) canvas. Set to `'null'` to disable, or pass a 6-char RGB HEX string (e.g., `'EBEBEB'`).

- Type=`str`, argtype=`temporary`
- The default value is `null`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_predictions</code></summary>

(bool) Controls whether to draw prediction during visualization.

- Type=`int`, argtype=`temporary`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_with_plt</code></summary>

(bool) Controls whether to use PLT (matplotlib) as the preferred method for visualizing trajectories on an empty canvas. If disabled, it attempts to visualize all points directly on the scene images.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--pred_color_mode</code></summary>

An integer indicating how stochastic predictions will be colored. It accepts the following values:

- `0`: Assign a random color to each specific prediction of each   agent to be forecasted (shaped with `t_f * dim`). - `1`: Assign the same random color to all predictions of a single   agent. - `2`: Assign the same random color to the $k$th stochastic prediction   of all agents to be forecasted.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--pred_color_seed</code></summary>

The random seed used to visualize model predictions. Set it to `0` to assign random colors for each prediction.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--text_scale</code></summary>

A float value used to scale the legend (text, icons, etc.) during visualization. A larger value means text and icons occupy a larger relative proportion of the screen. Must be greater than `0.2`.

- Type=`float`, argtype=`temporary`
- The default value is `-1.0`.

</details>

### Encore Args


<details markdown="1">
<summary markdown="span"><code>--Kg</code></summary>

The number of generations when making predictions. It is also the number of channels of the generating kernel in the proposed reverberation transform.

- Type=`int`, argtype=`static`
- The default value is `20`.

</details>

<details markdown="1">
<summary markdown="span"><code>--T</code> (short for <code>-T</code>)</summary>

Transform type used to compute trajectory spectrums.

Supported types: - `none`: No transformations. - `haar`: Haar wavelet transform. - `db2`: DB2 wavelet transform.

- Type=`str`, argtype=`static`
- The default value is `haar`.

</details>

<details markdown="1">
<summary markdown="span"><code>--compute_ego_bias</code></summary>

**Ablation Settings:** (bool) Controls whether to compute the ego bias, i.e., the cross-agent bilinear product in the ego predictor. It should only be turned off when performing ablation experiments.

- Type=`int`, argtype=`static`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--ego_capacity</code></summary>

The number of neighbors (`N`) to be "well-forecasted" by the ego predictor. When there are more than `N` neighbors in the scene, the ego predictor will choose the `N` closest neighbors relative to the ego agent to run the full-size prediction, while other neighbors will be forecasted using a simple linear predictor.

**Ablation Settings:** Note that the full-size Transformer-based ego predictor will be constructed and used for prediction only when `N > 0`. A linear predictor will be used for all neighbors when `N` is set to `0`.

- Type=`int`, argtype=`dynamic`
- The default value is `-1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--ego_loss_rate</code></summary>

Loss weight of the EgoLoss when training.

- Type=`float`, argtype=`static`
- The default value is `0.6`.

</details>

<details markdown="1">
<summary markdown="span"><code>--ego_t_f</code></summary>

Output length of the ego predictor.

- Type=`int`, argtype=`static`
- The default value is `-1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--ego_t_h</code></summary>

Input length of the ego predictor.

- Type=`int`, argtype=`static`
- The default value is `-1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--encode_agent_types</code></summary>

(bool) Controls whether to encode the type name of each agent. It is mainly used in multi-type-agent prediction scenes, providing a unique type-coding for each type of agent when encoding their trajectories.

- Type=`int`, argtype=`static`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--fix_insight_kernels</code></summary>

**Ablation Settings:** (bool) Controls whether to use the average agents' (in a batch) insight kernel to replace all other neighboring agents'. It should only be used for conducting further model discussions and *SHOULD NOT* be used during training. A typical experimental scene to use this arg is the `playground`, along side with the arg `predict_all_neighbors` and `pred_color_mode`  (both set to `1`).

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--insights</code></summary>

The number of "insights" (`I`) in the ego predictor. The full-size ego predictor will forecast `I` short-term trajectories for each neighbor within its capacity.

- Type=`int`, argtype=`static`
- The default value is `5`.

</details>

<details markdown="1">
<summary markdown="span"><code>--partitions</code></summary>

The number of partitions when computing the angle-based feature. It is only used when modeling social interactions.

- Type=`int`, argtype=`static`
- The default value is `-1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--use_intention_predictor</code></summary>

**Ablation Settings:** (bool) Controls whether to use the intention prediction as one of the model predictions.

- Type=`int`, argtype=`static`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--use_linear</code></summary>

**Ablation Settings:** (bool) Controls whether to use the linear prediction as the base of all other predictions.

- Type=`int`, argtype=`static`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--use_social_predictor</code></summary>

**Ablation Settings:** (bool) Controls whether to use the social prediction as one of the model predictions.

- Type=`int`, argtype=`static`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--vis_ego_predictor</code></summary>

Controls whether to visualize trajectories forecasted by the ego predictor. It accepts four kinds of string values:

- `0`: Do nothing *(Default)*. - `1`: Visualize all predictions of the ego predictor. - `2`: Visualize the ego predictor's mean prediction for each   neighbor. - `kn`: Visualize the *n*th rehearsals (from all $K_I$ insights).   For example, `--vis_ego_predictor k1`. NOTE that the *n* should be   less than the number of insights (controlled by arg `insights`).

NOTE that this arg only works in the *Playground* mode, or the program will be killed immediately.

- Type=`str`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--vis_insight_kernels</code></summary>

(bool) Controls whether to visualize the insight kernels learned by the ego predictor.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--vis_self_activations</code></summary>

Controls whether to visualize the feature selection results of the feature-level conditioning for the self-bias term. This only works when the intention predictor is enabled during training through the arg `use_intention_predictor`.

It accepts three values: - `0`: Do nothing *(Default)*. - `1`: Regular visualization. - `2`: Visualization while additionally displaying the activation of   the mean trajectory. - `3`: Visualize absolute feature deviation instead of activations.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--vis_social_activations</code></summary>

Controls whether to visualize the feature selection results of the feature-level conditioning for the social-bias term. This only works when the intention predictor is enabled during training through the arg `use_social_predictor`.

It accepts three values: - `0`: Do nothing *(Default)*. - `1`: Regular visualization. - `2`: Visualization while additionally displaying the activation of   the mean trajectory. - `3`: Visualize absolute feature deviation instead of activations.

Additionally, the default visualization neighbor is the zeroth neighbor (the ego itself) sorted by Euclidean distance. Neighbor IDs can be input as concatenated strings. For example, `1_3` refers to the third neighbor in mode 1 (Regular visualization).

- Type=`str`, argtype=`temporary`
- The default value is `0`.

</details>

### Playground Args


<details markdown="1">
<summary markdown="span"><code>--clip</code></summary>

The video clip to run this playground.

- Type=`str`, argtype=`temporary`
- The default value is `zara1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--compute_social_mod</code></summary>

(bool) Choose whether to enable the computing of social modifications.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--default_agent</code></summary>

Set the default index of agent to be predicted.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--do_not_draw_neighbors</code></summary>

(bool) Choose whether to draw neighboring-agents' trajectories.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--draw_seg_map</code></summary>

(bool) Choose whether to draw segmentation maps on the canvas.

- Type=`int`, argtype=`temporary`
- The default value is `1`.

</details>

<details markdown="1">
<summary markdown="span"><code>--lite</code></summary>

(bool) Choose whether to show the lite-version's visualization window.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--physical_manual_neighbor_mode</code></summary>

Mode for the manual neighbor on segmentation maps. - Mode `1`: Add obstacles to the given position; - Mode `0`: Set areas to be walkable.

- Type=`float`, argtype=`temporary`
- The default value is `1.0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--points</code></summary>

The number of points to simulate the trajectory of manual neighbor. It only accepts `2` or `3`.

- Type=`int`, argtype=`temporary`
- The default value is `2`.

</details>

<details markdown="1">
<summary markdown="span"><code>--predict_all_neighbors</code></summary>

(bool) Controls whether to predict trajectories for all other neighbors in the prediction scene.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--save_full_outputs</code></summary>

(bool) Choose whether to save all outputs as images.

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>

<details markdown="1">
<summary markdown="span"><code>--show_manual_neighbor_boxes</code></summary>

(Working in process)

- Type=`int`, argtype=`temporary`
- The default value is `0`.

</details>
<!-- DO NOT CHANGE THIS LINE -->
