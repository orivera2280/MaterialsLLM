import torch
import torch.nn.functional as F
import create_pytorch_data_object as DL

data_loader = DL.LocalDataLoader().get_data_loader('unified_dataset_10000.csv', 'data')

def setup_linear_layers(data_size, labels_size):
    lin_list = torch.nn.ModuleList()
    size_per_step = round((labels_size - data_size)/2, -3)
    for i in range(3):
        if i != 2:
            lin = torch.nn.Linear(data_size, int(data_size + size_per_step))
            data_size = int(data_size + size_per_step)
        else:
            lin = torch.nn.Linear(data_size, labels_size)
        lin_list.append(lin)

    return lin_list

data, labels = next(iter(data_loader))

model = setup_linear_layers(256, 8058)

loss_fn = torch.nn.L1Loss()
optim = torch.optim.Adam(model.parameters(), lr = 0.001)

for epoch in range(200):
    for batch, labels in data_loader:
        for i in range(len(model)):
            batch = model[i](batch)
            batch = F.relu(batch)

        loss = loss_fn(batch, labels)
        optim.zero_grad()
        loss.backward()
        optim.step()

    print('epoch:', epoch, ' loss: ', loss)
