### Use For Pretraining Dynamics Model
1. Model Structure
   * Backbone: Load Resnet18 pertrained on ResNet as Backbone
   * Train Mode: Dynamics Model head train in supervised mode
   1. Setting 1: Just train Dynamics Model head
   2. Setting 2: Simultaneously train Dynamics Model head and backbone
2. Data Collection
   * Collect Data in Created Environment in Webots
3. Configuration
   * Config file: **pretrain_cfg.json**
   * Attribute:
     * **Mode:** Training Mode
       * "Head_only": Train Dynamics Model Head Only
       * "Head_backbone": Train Dynamics Model Head and Backbone simultaneously
     * **State_Buffer:** Number of Frame use as Input
     * **Batch_size:** Batch size
     * **Action_Buffer:** Number of Action use as Input
     * **Evolution_step:** Number of Step the Evolution Block need to Evolute 
     * **Model_Type:** Pretrained Model Type
       * "resnet18": 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
       * "resnet34": 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
     * **Hidden_dim** dimension of fully connected layer(list of 2 -- 3 layer FCN)
     * **State_size:** Input image size
     * **State_channel:** use Grayscale or RGB image as state 
     * **Backbone:** Specify Network Backbone(Block to use in training)
     * **Action_dim:** Dimension of action
     * **Number_Action:** Number of action
       * Default:1 Only predict 1 possible future action
       * >1: Predict more than one possible action(get final action by weighted sum of confidence)
     * **Confidence:** Whether need to predict confidence of Results(Default:False)
4. **Usage**
  1. Change Directory to `PRETRAIN_DM/`
  2. Get OriginDataset: Follow instructions in file `OriginDataset/README.md`
  3. Run `pretrain_datapreprocess.py` script to get data ready according to pretrain_cfg.json
  4. Run `pretrain_datasplit.py` script to generate train and test set in folder `DynamicsDataset/Batch${Batch_size}State${State_Buffer}`
  5. 