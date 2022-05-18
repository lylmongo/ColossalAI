from copy import copy
import torch
from colossalai.tensor.op_wrapper import colo_op_impl
from colossalai.tensor import ColoTensor
from ._utils import GeneralTensor

# @colo_op_impl(torch.mean)
# def colo_mean(types, args=(), kwargs=None, pg=None):
#     input_t = args[0]
#     if isinstance(input_t, ColoTensor):
#         input_t = input_t.torch_tensor()
#     return ColoTensor.init_from_torch_tensor(torch.mean(input_t))


def register_elementwise_op(op):

    @colo_op_impl(op)
    def elementwise_op(input_tensor: GeneralTensor, *args, **kwargs):
        """
        Handles ``__torch_function__`` dispatch for the elementwise op such
        as ``torch.nn.functional.gelu`` or ``torch.nn.functional.relu``.
        This method computes on either a normal tensor or a sharded tensor.
        """
        output = op(input_tensor, *args, **kwargs)
        if isinstance(input_tensor, ColoTensor):
            spec = copy(input_tensor.spec)
            return ColoTensor.from_torch_tensor(output, spec=spec)
        return ColoTensor.from_torch_tensor(output)


register_elementwise_op(torch.nn.functional.gelu)
register_elementwise_op(torch.nn.functional.relu)
register_elementwise_op(torch.clone)
register_elementwise_op(torch.Tensor.clone)
register_elementwise_op(torch.Tensor.detach)

# @colo_op_impl(torch.sum)
# def sum_op(types, args=(), kwargs=None, pg=None):
#     """
#     Handles ``__torch_function__`` dispatch for the elementwise op such
#     as ``torch.sum`.
#     This method computes on either a normal tensor or a sharded tensor.
#     """
#     if len(args) > 0:
#         input_tensor = args[0]
#     if kwargs is None:
#         kwargs = {}
#     if 'input' in kwargs:
#         input_tensor = kwargs['input']
#     # Validate types
#     if not isinstance(input_tensor, ColoTensor):
#         raise TypeError("input needs to be a ColoTensor")
#     return ColoTensor.init_from_torch_tensor(torch.sum(input_tensor.torch_tensor()))
