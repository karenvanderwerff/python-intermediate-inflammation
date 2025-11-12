from unittest.mock import Mock, patch


def test_analyse_data_mock_source():
    from inflammation.compute_data import analyse_data

    data_source = Mock()
    data_source.load_inflammation_data.return_value = [[[1, 2, 3]], [[4, 5, 6]]]

    # Patch the visualization so it doesn't block the test
    with patch("inflammation.compute_data.views.visualize"):
        analyse_data(data_source)
