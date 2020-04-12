sample_view_info = [
    {
        "view":  
        {
            "view_name": 'view_name_1',
            "columns": 
            [
                {
                    "column_name": 'column_name', 
                    "column_type": 'int'
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
                    "column_type": 'int'
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
                    "column_type": 'int'
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
    {'message': 'Outputs for explore_data()'},
    {
        "download": True,
        "single_file": False,
        "data":
        [
            {
                "view_names": ['view_name'],
                "column_names": [ 'colname', 'colname', 'colname'],
                "data":
                [
                    ['datum', 'datum', 'datum'],  # first row of data
                    ['datum', 'datum', 'datum'],
                    ['datum', 'datum', 'datum'],
                ],
            }, # end first dataset
            {
                "view_names": ['view_name'],
                "column_names": [ 'colname', 'colname'],
                "data":
                [
                    ['datum', 'datum'],  # first row of data
                    ['datum', 'datum'],
                    ['datum', 'datum'],
                ],
            } #  end second dataset
        ] ,  # end data array
    }, 

    {
    "download": False,
    "files_to_prepare": 0,
    "data":
    [
    {
        "view_names": ['view_name', 'view_name'], 
        "column_names":
        [
            'colname',
            'colname',
            'colname',
            'colname',
            'colname'
        ],
        "data":
        [
            ['datum', 'datum', 'datum', 'datum', 'datum'],
            ['datum', 'datum', 'datum', 'datum', 'datum'],
            ['datum', 'datum', 'datum', 'datum', 'datum'],


                ],
                }, # end first dataset
                # additional datasets will be ignored if download is false
                ] ,  # end data array

    }, 
] 
