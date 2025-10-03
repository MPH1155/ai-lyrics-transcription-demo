import os
from audio_separator.separator import Separator

def seperate_vocals_instrumental(input_path, output):
    separator = Separator(output_dir=output)
    separator.load_model(model_filename='model_bs_roformer_ep_317_sdr_12.9755.ckpt')

    file_name = os.path.basename(input_path)
    # Vocals and Instrumental
    vocals = os.path.join(output, f'Vocals_{file_name[:-4]}.wav')
    instrumental = os.path.join(output, f'Instrumental_{file_name[:-4]}.wav')
    
    # Splitting a track into Vocal and Instrumental
    voc_inst = separator.separate(input_path)
    os.rename(os.path.join(output, voc_inst[0]), instrumental) # Rename file to “Instrumental_<filename>.wav”
    os.rename(os.path.join(output, voc_inst[1]), vocals) # Rename file to “Vocals_<filename>.wav”
    return vocals

if __name__ == "__main__":
    input_dir = "fromthescreen/"#@param {type:"string"}
    output = "data/audio/"#@param {type:"string"}

    separator = Separator(output_dir=output)
    separator.load_model(model_filename='model_bs_roformer_ep_317_sdr_12.9755.ckpt')

    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        
        # Vocals and Instrumental
        vocals = os.path.join(output, f'Vocals_{file_name[:-4]}.wav')
        instrumental = os.path.join(output, f'Instrumental_{file_name[:-4]}.wav')


        # Splitting a track into Vocal and Instrumental
        
        voc_inst = separator.separate(input_path)
        os.rename(os.path.join(output, voc_inst[0]), instrumental) # Rename file to “Instrumental_<filename>.wav”
        os.rename(os.path.join(output, voc_inst[1]), vocals) # Rename file to “Vocals_<filename>.wav”
    

