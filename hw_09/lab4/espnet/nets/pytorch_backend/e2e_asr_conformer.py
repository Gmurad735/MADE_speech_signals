# Copyright 2020 Johns Hopkins University (Shinji Watanabe)
#                Northwestern Polytechnical University (Pengcheng Guo)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

"""
Conformer speech recognition model (pytorch).

It is a fusion of `e2e_asr_transformer.py`
Refer to: https://arxiv.org/abs/2005.08100

"""

from espnet.nets.pytorch_backend.conformer.encoder import Encoder
from espnet.nets.pytorch_backend.e2e_asr_transformer import E2E as E2ETransformer
from espnet.nets.pytorch_backend.conformer.argument import (
    add_arguments_conformer_common,  # noqa: H301
)


class E2E(E2ETransformer):
    """E2E module.

    :param int idim: dimension of inputs
    :param int odim: dimension of outputs
    :param Namespace args: argument Namespace containing options

    """

    @staticmethod
    def add_arguments(parser):
        """Add arguments."""
        E2ETransformer.add_arguments(parser)
        E2E.add_conformer_arguments(parser)
        return parser

    @staticmethod
    def add_conformer_arguments(parser):
        """Add arguments for conformer model."""
        group = parser.add_argument_group("conformer model specific setting")
        group = add_arguments_conformer_common(group)
        return parser

    def __init__(self, idim, odim, args, ignore_id=-1):
        """Construct an E2E object.

        :param int idim: dimension of inputs
        :param int odim: dimension of outputs
        :param Namespace args: argument Namespace containing options
        """
        super().__init__(idim, odim, args, ignore_id)
        if args.transformer_attn_dropout_rate is None:
            args.transformer_attn_dropout_rate = args.dropout_rate
        self.encoder = Encoder(
            idim=idim,
            attention_dim=args.adim,
            attention_heads=args.aheads,
            linear_units=args.eunits,
            num_blocks=args.elayers,
            input_layer=args.transformer_input_layer,
            dropout_rate=args.dropout_rate,
            positional_dropout_rate=args.dropout_rate,
            attention_dropout_rate=args.transformer_attn_dropout_rate,
            pos_enc_layer_type=args.transformer_encoder_pos_enc_layer_type,
            selfattention_layer_type=args.transformer_encoder_selfattn_layer_type,
            activation_type=args.transformer_encoder_activation_type,
            macaron_style=args.macaron_style,
            use_cnn_module=args.use_cnn_module,
            cnn_module_kernel=args.cnn_module_kernel,
            use_chunk=args.use_chunk,
            chunk_window=args.chunk_window,
            chunk_left_context=args.chunk_left_context,
            chunk_right_context=args.chunk_right_context,
            use_checkpointing=args.grad_checkpointing,
        )
        self.reset_parameters(args)
