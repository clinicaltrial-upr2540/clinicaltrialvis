sample_view_info = [
    {
        "view":
        {
            "view_name": 'view_name_1',
            "columns":
            [
                {
                    "column_name": 'column_name',
                    "column_type": 'integer'
                },
                {
                    "column_name": 'column_name',
                    "column_type": 'text'
                },
                {
                    "column_name": 'column_name',
                    "column_type": 'text'
                },
            ]
        }
    },


    {
        "view":
        {
            "view_name": 'view_name_2',
            "columns":
            [
                {
                    "column_name": 'column_name',
                    "column_type": 'integer'
                },
                {
                    "column_name": 'column_name',
                    "column_type": 'text'
                },
                {
                    "column_name": 'column_name',
                    "column_type": 'text'
                },
                {
                    "column_name": 'column_name',
                    "column_type": 'integer'
                },
                {
                    "column_name": 'column_name',
                    "column_type": 'text'
                },
            ]
        }
    }

]

list_of_responses = [
    {
        "download": True,
        "single_file": False,
        "data":
            [
                {
                    "view_names": ['view1'],
                    "column_names": ['colname', 'colname', 'colname'],
                    "data":
                    [
                        ['datum', 'datum', 'datum'],  # first row of data
                        ['datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum'],
                    ],
                },  # end first dataset
                {
                    "view_names": ['view_name'],
                    "column_names": [ 'colname', 'colname'],
                    "data":
                    [
                        ['datum', 'datum'],  # first row of data
                        ['datum', 'datum'],
                        ['datum', 'datum'],
                    ],
                }  #  end second dataset
            ],  # end data array
    },

    {
    "download": False,
    "data":
        [
            {
                "view_names": ['view1', 'view2'],
                "column_names":
                    [
                        ['view1', 'colname'],
                        ['view1', 'colname'],
                        ['view2', 'colname'],
                        ['view2', 'colname'],
                        ['view2', 'colname']
                    ],
                "data":
                    [
                        ['datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum'],
                    ],
            },  # end first dataset
            # additional datasets will be ignored if download is false
        ] ,  # end data array

    },

    {
    "download": False,
    "data":
        [
            {
                "view_names": ['view1', 'view2'],
                "column_names":
                    [
                        ['view1', 'colname'],
                        ['view1', 'colname'],
                        ['view2', 'colname']
                    ],
                "data":
                    [
                        ['datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum'],
                    ],
            },  # end first dataset
            # additional datasets will be ignored if download is false
        ],  # end data array

    },

    {
    "download": False,
    "data":
        [
            {
                "view_names": ['view1', 'view2'],
                "column_names":
                    [
                        ['view1', 'colname'],
                        ['view1', 'colname'],
                        ['view1', 'colname'],
                        ['view1', 'colname'],
                        ['view1', 'colname'],
                        ['view2', 'colname'],
                        ['view2', 'colname']
                    ],
                "data":
                    [
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                        ['datum', 'datum', 'datum', 'datum', 'datum', 'datum', 'datum'],
                    ],
            },  # end first dataset
            # additional datasets will be ignored if download is false
        ],  # end data array

    },
]
