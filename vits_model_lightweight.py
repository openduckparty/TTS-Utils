import torch

if __name__ == '__main__':
    model_path = "saved_model/model.pth"
    output_path = "saved_model/model1.pth"
    checkpoint_dict = torch.load(model_path, map_location='cpu')
    checkpoint_dict_new = {}
    for k, v in checkpoint_dict.items():
        if k == "optimizer":
            print("remove optimizer")
            continue
        checkpoint_dict_new[k] = v
    torch.save(checkpoint_dict_new, output_path)
