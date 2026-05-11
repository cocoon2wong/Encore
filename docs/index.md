---
layout: page
title: Encore
subtitle: "Encore: Conditioning Trajectory Forecasting via Biased Ego Rehearsals"
cover-img: /subassets/img/head.jpg
---
<!--
 * @Author: Conghao Wong
 * @Date: 2026-01-29 19:48:42
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2026-05-11 11:37:28
 * @Github: https://cocoon2wong.github.io
 * Copyright 2026 Conghao Wong, All Rights Reserved.
-->

## Information

This is the homepage of our paper "Encore: Conditioning Trajectory Forecasting via Biased Ego Rehearsals".
Full paper will be made on arXiv soon.
Click the following buttons for more information:

<div class="btn-normal-group" style="text-align: center;">
    <!-- {% if site.arxiv-id %} -->
    <!-- <a class="btn btn-lg btn-normal" href="./paper">📖 Paper</a> -->
    <!-- {% endif %} -->
    <a class="btn btn-lg btn-normal" href="{{ site.github.repository_url }}">🛠️ Code</a>
    <a class="btn btn-lg btn-normal" href="./weights">🛠️ Weights</a>
    <a class="btn btn-lg btn-normal" href="./guidelines">💡 Code Guidelines</a>
    <br><br>
</div>

## Abstract

Learning and representing the subjectivities of agents has become a challenging but crucial problem in the trajectory prediction task.
Such subjectivities not only present specific spatial or temporal structures, but also are anisotropic for all interaction participants.
Despite great efforts, it remains difficult to explicitly learn and forecast these subjectivities, let alone further modulate models' predictions through a specific ego's subjectivity.
Inspired by prefactual thoughts in psychology and relevant theatrical concepts, we interpret such subjectivities in future trajectories as the continuous process from rehearsal to encore.
In the rehearsal phase, the proposed ego predictor focuses on how each ego agent learns to derive and direct a set of explicitly biased rehearsal trajectories for all participants in the scene from the short-term observations.
Then, these rehearsal trajectories serve as immediate controls to condition final predictions, providing direct yet distinct ego biases for the prediction network to simulate agents' various subjectivities.
Experiments across datasets not only demonstrate a consistent improvement in the performance of the proposed *Encore* trajectory prediction model but also provide clear interpretability regarding subjectivities as biased ego rehearsals.

<div style="text-align: center">
  <img src="https://raw.githubusercontent.com/cocoon2wong/Encore/main/docs/subassets/img/motivation.png" alt="Motivation Illustration" height="500">
  <p></p>
</div>

> Fig. Motivation illustration.
> The processes of both social interactions and trajectory planning are mostly structured and anisotropic, starting from how agents uniquely perceive and then construct their own biased interactive contexts.
> Inspired by theatrical concepts, we restructure trajectory prediction into two consecutive phases.
> Each agent first uses its own ego bias to consider all participants in the scene, directing a set of short but structured biased rehearsal trajectories as its exclusive interaction context.
> Then, it produces the final live performance based on these unique rehearsals, thereby conditioning interactions and trajectories on specific ego biases.

## Method Overview

The proposed *Encore* trajectory prediction model consists of two main parts, the `Ego Predictor` and the `Final Predictor`.
Both predictors collaborate to achieve conditioned predictions, guided by the rehearsal trajectories (*i.e.*, biased short-term future predicted trajectories) *directed* by each ego agent.
As illustrated, before the final forecasting, the ego predictor first provides a set of biased short-term rehearsals for the ego agent itself and all its neighbors, learning and forecasting how each ego agent uniquely considers its future trajectory plans as well as interaction contexts.
These rehearsals will be concatenated with their original observations and then fed to the final predictor with specific conditioning rules, achieving the goal of asymmetric bias-conditioned trajectory prediction.
This section first formulates the proposed ego predictor, then introduces how the *Encore* model is constructed and trained.

<div style="text-align: center">
  <img src="https://raw.githubusercontent.com/cocoon2wong/Encore/main/docs/subassets/img/method_overall.png" alt="Method Overview">
  <p></p>
  <img src="https://raw.githubusercontent.com/cocoon2wong/Encore/main/docs/subassets/img/method_ego_predictor.png" alt="Ego Predictor Overview">
  <p></p>
</div>

> Overall computation pipeline of the proposed *Encore* model (up) and detailed structures of the ego predictor (down) when running the regular forecasting.
> For the ego predictor, an additional computation will be performed on observation and prediction periods $\mathcal{T}_a$ and $\mathcal{T}_b$ (corresponding to periods $\mathcal{T}_c$ and $\mathcal{T}_d$ in the figure) to learn ego biases under the joint optimization of the proposed ego loss (\EQUA{eq_ego_loss}) and the regular $\ell_2$ loss.
