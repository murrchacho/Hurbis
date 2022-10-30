import { useContext } from 'react';
import { AuthContext } from '../HOCs/All';

export function useAuth() {
    return useContext(AuthContext);
}
