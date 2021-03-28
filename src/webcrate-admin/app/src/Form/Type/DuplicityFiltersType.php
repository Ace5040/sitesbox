<?php

namespace App\Form\Type;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\CollectionType;

class DuplicityFiltersType extends AbstractType
{

    public function getParent(): string
    {
        return CollectionType::class;
    }
}
