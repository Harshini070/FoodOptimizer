from django import forms

class FoodDistributionForm(forms.Form):
    supply = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), help_text="Comma-separated food available at centers")
    demand = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), help_text="Comma-separated food needed at shelters")
    cost_matrix = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), help_text="Cost matrix (comma-separated rows, one per line)")


class OptimizationForm(forms.Form):
    supply = forms.CharField(widget=forms.Textarea, label='Supply')
    demand = forms.CharField(widget=forms.Textarea, label='Demand')
    cost_matrix = forms.CharField(widget=forms.Textarea, label='Cost matrix')