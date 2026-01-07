import stripe
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Item


def item_view(request, id):
		item = get_object_or_404(Item, pk=id)
		publishable = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
		html = f"""
		<html>
			<head>
				<title>Buy {item.name}</title>
			</head>
			<body>
				<h1>{item.name}</h1>
				<p>{item.description}</p>
				<p>Price: {item.price} ({item.currency})</p>
				<button id="buy-button">Buy</button>
				<script src="https://js.stripe.com/v3/"></script>
				<script>
					var stripe = Stripe('{publishable}');
					var buyButton = document.getElementById('buy-button');
					buyButton.addEventListener('click', function() {{
						fetch('/buy/{item.id}', {{method: 'GET'}})
						.then(function(res) {{ return res.json(); }})
						.then(function(session) {{
								return stripe.redirectToCheckout({{ sessionId: session.id }});
						}})
						.then(function(result) {{
							if (result && result.error) {{
								alert(result.error.message);
							}}
						}});
					}});
				</script>
			</body>
		</html>
		"""
		return HttpResponse(html)


def buy_view(request, id):
		item = get_object_or_404(Item, pk=id)
		secret = getattr(settings, 'STRIPE_SECRET_KEY', '')
		if not secret:
				return JsonResponse({'error': 'Stripe secret key not configured'}, status=500)
		stripe.api_key = secret
		# build absolute urls for success and cancel
		host = request.build_absolute_uri('/')[:-1]
		success_url = host + '/'
		cancel_url = host + '/'

		try:
				# validate currency and fallback to default if unsupported
				supported = getattr(settings, 'SUPPORTED_STRIPE_CURRENCIES', None)
				default_currency = getattr(settings, 'STRIPE_DEFAULT_CURRENCY', 'usd')
				currency = item.currency.lower() if item.currency else default_currency
				if supported is not None and currency not in supported:
					currency = default_currency

				session = stripe.checkout.Session.create(
						payment_method_types=['card'],
						line_items=[{
								'price_data': {
								'currency': currency,
										'product_data': {
												'name': item.name,
												'description': item.description,
										},
										'unit_amount': item.price,
								},
								'quantity': 1,
						}],
						mode='payment',
						success_url=success_url,
						cancel_url=cancel_url,
				)
		except Exception as e:
				return JsonResponse({'error': str(e)}, status=500)

		return JsonResponse({'id': session.id})
