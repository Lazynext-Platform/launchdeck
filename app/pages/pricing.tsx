// File: app/pages/pricing.tsx
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { API_URLS } from '~/constants/api';
import { PricingPlan } from '~/types/pricing';
import { shadcn } from '@shadcn/ui/react';
import { Loading } from '~/components/Loading';
import { Error } from '~/components/Error';

const PricingPage = () => {
  const [plans, setPlans] = useState<PricingPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPlans = async () => {
    try {
      const response = await fetch(API_URLS.pricing);
      const data = await response.json();
      setPlans(data);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlans();
  }, []);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <Error message={error.message} />;
  }

  return (
    <div className="max-w-5xl mx-auto p-4 md:p-6 lg:p-8 mt-10 mb-20">
      <h1 className="text-3xl font-bold mb-4">Pricing Plans</h1>
      <div className="flex flex-wrap justify-center -mx-4">
        {plans.map((plan) => (
          <div
            key={plan.id}
            className="w-full md:w-1/2 xl:w-1/3 p-4 mb-8 md:mb-0"
          >
            <shadcn.Card>
              <shadcn.CardHeader>
                <h2 className="text-xl font-bold">{plan.name}</h2>
              </shadcn.CardHeader>
              <shadcn.CardBody>
                <p className="text-lg">{plan.description}</p>
                <p className="text-2xl font-bold">${plan.price}/month</p>
                <ul>
                  {plan.features.map((feature) => (
                    <li key={feature}>{feature}</li>
                  ))}
                </ul>
              </shadcn.CardBody>
              <shadcn.CardFooter>
                <shadcn.Button>Subscribe</shadcn.Button>
              </shadcn.CardFooter>
            </shadcn.Card>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PricingPage;