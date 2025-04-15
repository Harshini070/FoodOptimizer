from django.shortcuts import render, redirect
import numpy as np
from scipy.optimize import linprog
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import ast
import io
import csv
import json

# Show the input form
def input_view(request):
    return render(request, 'index.html')

# Handle form submission and show result
def optimize_distribution(request):
    if request.method == 'POST':
        try:
            # Parse supply and demand as integers
            supply = list(map(int, request.POST['supply'].split(',')))
            demand = list(map(int, request.POST['demand'].split(',')))

            # Load cost_matrix from JSON and ensure it's all floats
            raw_matrix = json.loads(request.POST['cost_matrix'])
            cost_matrix = [[float(cell) for cell in row] for row in raw_matrix]

            if len(supply) != len(cost_matrix) or any(len(row) != len(demand) for row in cost_matrix):
                return render(request, 'result.html', {
                    'result': "Error: Supply/Demand dimensions don't match the cost matrix."
                })

            # Linear programming setup
            c = np.array(cost_matrix).flatten()
            A_eq, b_eq = [], []

            # Supply constraints
            for i in range(len(supply)):
                row = [0] * len(c)
                for j in range(len(demand)):
                    row[i * len(demand) + j] = 1
                A_eq.append(row)
                b_eq.append(supply[i])

            # Demand constraints
            for j in range(len(demand)):
                row = [0] * len(c)
                for i in range(len(supply)):
                    row[i * len(demand) + j] = 1
                A_eq.append(row)
                b_eq.append(demand[j])

            bounds = [(0, None)] * len(c)
            res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

            if res.success:
                x = res.x.reshape((len(supply), len(demand)))
                result = x.round(2).tolist()
                total_cost = round(np.sum(x * np.array(cost_matrix, dtype=float)), 2)
            else:
                result = "Optimization failed!"
                total_cost = None

            return render(request, 'result.html', {
                'result': result,
                'total_cost': total_cost
            })

        except Exception as e:
            return render(request, 'result.html', {'result': f"Error: {str(e)}"})

    return redirect('input_view')


@csrf_exempt
def download_csv(request):
    if request.method == 'POST':
        result = ast.literal_eval(request.POST['csv_data'])
        total_cost = request.POST['total_cost']

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['From / To'] + [f'Shelter {i+1}' for i in range(len(result[0]))])

        for i, row in enumerate(result):
            writer.writerow([f'Center {i+1}'] + row)

        writer.writerow([])
        writer.writerow(['Total Transportation Cost', total_cost])

        response = HttpResponse(buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=optimized_distribution.csv'
        return response
