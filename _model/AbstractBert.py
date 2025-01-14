import torch
from torch import nn
import numpy as np

from transformers import *
from torch.nn import CrossEntropyLoss

class AbstractBert(nn.Module):
  
    def __init__(self, vocab: str='bert-base-uncased', num_labels: int=2):
        """ BERT model with customizable layers for classification. 
        Keyword Arguments:
            pretrained_weights {str} -- pretrained weights to load BERT with (default: {'bert-base-uncased'})
            num_labels {int} -- number of labels for the data (default: {2})
        """          
        super(AbstractBert, self).__init__()
    
        self.num_labels = num_labels
        self.vocab = vocab

        # output: last_hidden_state, pooler_output, hidden_states
        config = AutoConfig.from_pretrained(vocab, output_hidden_states=True)
        self.bert = AutoModel.from_pretrained(vocab, config = config)

        # self.bert = BertModel.from_pretrained(pretrained_weights, output_hidden_states=True)
        # self.dropout = nn.Dropout(0.3)

        ########### NOTE, optional: add or change classifier on top of BERT here ###########
        # self.classifier = nn.Linear(config.hidden_size, num_labels)
        # nn.init.xavier_normal_(self.classifier.weight)
        ########### NOTE, optional: add or change classifier on top of BERT here ########### 

    def forward(self, input_ids, augment_ids = None, token_type_ids=None, attention_mask=None, labels=None, augmented=None):
        """ Forward method of the BERT model. 
        Arguments:
            input_ids {torch.tensor} -- unique identifier of the input.
            augment_ids {torch.tensor} -- unique identifier of the augmented input.
        Keyword Arguments:
            token_type_ids {torch.tensor} -- sentence type. (default: {None})
            attention_mask {torch.tensor} -- mask for padding. (default: {None})
            labels {torch.tensor} --  labels for the data. (default: {None})
            augmented {torch.tensor} -- metadata embeddings to augment the pooled output (default: {None})
        Returns:
            torch.tensor -- pooled output token or logits
        """  

        '''
        NOTE: 
        The pooled output is the learned pooled representation of the entire input.
        If we want to manually learn a new representation, we want to take the last 4 layers
        to get an embedding for a single token.
        Then, we would need to learn a new representation (e.g., 1D CNN) between all these embeddings 
        for the entire input (averaging all the embeddings will lose more info compared to using [CLS] token). 
        '''
        
        _, pooled_output, hidden_states = self.bert(input_ids, token_type_ids, attention_mask)
        # pooled_output = self.dropout(pooled_output)

        # TODO: better metric than average? get an average of all the items in the augmented embeddings
        # if augment_ids is not None:
        #     augment_ids = [x[0].clone().detach().requires_grad_(True) for x in augment_ids]
        #     avg_emb = torch.mean(torch.stack(augment_ids), dim=0)
        #     # concat the augementation to the pooled output
        #     pooled_output_augmented = torch.cat((pooled_output, avg_emb), dim=1)

            ########### NOTE, OPTIONAL: send in the augmented embeddings through classifier ###########
            # logits = self.classifier(pooled_output_augmented)
            # return logits
            ########### NOTE, OPTIONAL: send in the augmented embeddings through classifier ###########

        #     return pooled_output_augmented
        # else: 

        return pooled_output