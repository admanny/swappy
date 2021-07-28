import swap
import pytest
import argparse

from unittest import mock


class TestSwap():
    input_token='0x0000000000000000000000000000000000000000'
    output_token='0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d'
    quantity='1'

    def test_get_swap_config(self):
        config = swap.get_swap_config()
        
        assert config is not None
        assert config.get('my_pk')

    def test_parse_args(self):
        test_parser = swap.parse_args(['-i', self.input_token,
                                    '-o', self.output_token,
                                    '-q', self.quantity])
        
        assert test_parser.input_token == self.input_token
        assert test_parser.output_token == self.output_token
        assert test_parser.qty == self.quantity
        with pytest.raises(AttributeError):
            test_parser.invalid_arg

    @mock.patch('swap.Web3', autospec=True)
    @mock.patch('swap.get_token_decimals', return_value = 18)
    def test_get_token_decimals(self, mock_func, mock_web3):
        decimal = swap.get_token_decimals(self.input_token, mock_web3)
        assert decimal == 18

    @mock.patch('swap.parse_args', return_value=argparse.Namespace(input_token=input_token, output_token=output_token,qty=quantity))
    @mock.patch('swap.Web3', autospec=True)
    @mock.patch('swap.get_token_decimals', return_value=18)
    @mock.patch('swap.Pancakeswap', autospec=True)
    def test_main(self, mock_pcs, mock_token_func, mock_web3, mock_args):
        swap.main()
        
        mock_pcs.assert_called_once()
        mock_token_func.assert_called_once()
        mock_web3.assert_called()
        mock_args.assert_called_once()
