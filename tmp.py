# import os
# import sys

# import torch
# import torchaudio
# from einops import rearrange
# from pathlib import Path
# import argparse

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# from open_musiclm.config import load_model_config, create_musiclm_from_config

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='run inference on trained musiclm model')

#     prompt = ['The main soundtrack of an arcade game. It is fast-paced and upbeat, with a catchy electric guitar riff. The music is repetitive and easy to remember, but with unexpected sounds, like cymbal crashes or drum rolls']

    

#     CHECKPOINT_PATH = './checkpoint/music/'
#     model_config = load_model_config(f'{CHECKPOINT_PATH}/musiclm_large_small_context.json')
#     semantic_path = f'{CHECKPOINT_PATH}/semantic.transformer.14000.pt'
#     coarse_path = f'{CHECKPOINT_PATH}/coarse.transformer.18000.pt'
#     fine_path = f'{CHECKPOINT_PATH}/fine.transformer.24000.pt'
#     input_audio = None
#     return_coarse_wave = False
#     duration = 60
#     kmeans_path = f'{CHECKPOINT_PATH}/kmeans_10s_no_fusion.joblib'
#     rvq_path = f'{CHECKPOINT_PATH}/clap.rvq.950_no_fusion.pt'
#     seed = 0
#     results_folder = f'outputs'

#     Path(results_folder).mkdir(parents=True, exist_ok=True)

#     device = 'cuda' if torch.cuda.is_available() else 'cpu'
#     print("///////////////")
#     print(device)
#     musiclm = create_musiclm_from_config(
#         model_config=model_config,
#         semantic_path=semantic_path,
#         coarse_path=coarse_path,
#         fine_path=fine_path,
#         rvq_path=rvq_path,
#         kmeans_path=kmeans_path,
#         device=device)

#     torch.manual_seed(seed)

#     print(f'prompt: {prompt}')

#     prime_wave, prime_wave_sample_hz = None, None
#     if input_audio is not None:
#         prime_wave, prime_wave_sample_hz = torchaudio.load(input_audio)
#         prime_wave = prime_wave.to(device)

#     generated_wave, similarities = musiclm.generate_top_match(
#         text=prompt,
#         prime_wave=prime_wave,
#         prime_wave_sample_hz=prime_wave_sample_hz,
#         num_samples=1,
#         num_top_matches=1,
#         output_seconds=duration,
#         semantic_window_seconds=model_config.global_cfg.semantic_audio_length_seconds,
#         coarse_window_seconds=model_config.global_cfg.coarse_audio_length_seconds,
#         fine_window_seconds=model_config.global_cfg.fine_audio_length_seconds,
#         semantic_steps_per_second=model_config.hubert_kmeans_cfg.output_hz,
#         acoustic_steps_per_second=model_config.encodec_cfg.output_hz,
#         return_coarse_generated_wave=return_coarse_wave,
#     )

#     for i, (wave, sim) in enumerate(zip(generated_wave, similarities)):
#         wave = rearrange(wave, 'b n -> b 1 n').detach().cpu()
#         print(f'prompt: {prompt[i]}')
#         print(f'topk similarities: {sim}')
#         for j, w in enumerate(wave):
#             torchaudio.save(Path(results_folder) / Path(f'{prompt[i][:35]}_top_match_{j}.wav'), w, musiclm.neural_codec.sample_rate)
import re
multiline_string = '''1. "The only way to do great work is to love what you do" - Steve Jobs
2. "The best way to predict the future is to create it" - Abraham Lincoln
3. "Change is the only constant in life" - Heraclitus
4. "It always seems impossible until it's done" - Nelson Mandela
5. "No one can make you feel inferior without your consent" - Eleanor Roosevelt'''

# 줄바꿈 대신 이중 줄바꿈을 사용해 다시 정리
formatted_string = re.sub(r'^[\d.]*\s*', '', multiline_string)

# 결과 출력
print(formatted_string)